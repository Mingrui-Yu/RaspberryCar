import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import time
from enum import Enum

from picamera.array import PiRGBArray
from picamera import PiCamera

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared
from camera import CarCamera
from track import CarDetect

GPIO.setwarnings(False)  # Disable warning
GPIO.setmode(GPIO.BCM)  # BCM coding


# # 远程调试用代码,如果不使用pycharm进行调试，请注释该段代码
# import sys
#
# sys.path.append("pydevd_pycharm.egg")
# import pydevd_pycharm
#
# pydevd_pycharm.settrace('192.168.12.162', port=20000, stdoutToServer=True, stderrToServer=True)
#
#
# # =======================


class CarState(Enum):
    stop = 0
    go = 1
    fast_go = 2
    light_left = 3
    left = 4
    heavy_left = 5
    light_right = 6
    right = 7
    heavy_right = 8


class Car(CarMove, CarUltrasound, CarInfrared, CarCamera, CarDetect):  # create class Car, which derives all the modules
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)
        CarCamera.__init__(self)
        CarDetect.__init__(self)
        self.state = CarState.stop

    def AllStop(self):
        self.state = CarState.stop
        CarMove.MotorStop(self)
        CarCamera.CameraCleanup(self)
        GPIO.cleanup()


def center_refresh(center_list, new_center, index):
    if new_center >= 0:
        index = (index + 1) % 5
        if len(center_list) < 5:
            center_list.append(new_center)
        else:
            center_list[index] = new_center
    if len(center_list) > 0:
        return np.median(center_list) * 0.7 + new_center * 0.3 - 320, center_list
    else:
        return 0, center_list


if __name__ == '__main__':
    try:
        car = Car()

        VideoReturn = True
        near_list = []
        medium_list = []
        far_list = []
        near_index = 0
        medium_index = 0
        far_index = 0

        camera, rawCapture = car.CameraInit()  # Initialize the PiCamera
        for raw_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            t_start = time.time()  # 用来计算FPS

            frame_origin = raw_frame.array

            if VideoReturn:  # detect the tennis & transmit the frames to PC
                frame_detect, near_center, medium_center, far_center = car.LineTrack(frame_origin, VideoReturn)
                car.VideoTransmission(frame_detect)
            else:
                near_center, medium_center, far_center = car.LineTrack(frame_origin, VideoReturn)

            if near_center < 0:
                if medium_center < 0:
                    if far_center < 280:
                        car.state = CarState.left
                    elif far_center < 360:
                        car.state = CarState.go
                    else:
                        car.state = CarState.right
                else:
                    if medium_center < 280:
                        car.state = CarState.left
                    elif medium_center < 360:
                        car.state = CarState.go
                    else:
                        car.state = CarState.right
            elif far_center < 0 or medium_center < 0:
                if near_center < 280:
                    car.state = CarState.left
                elif near_center < 360:
                    car.state = CarState.go
                else:
                    car.state = CarState.right
            else:
                # 效果不佳
                # near_bias, near_list = center_refresh(near_list, near_center, near_index)
                # medium_bias, medium_list = center_refresh(medium_list, medium_center, medium_index)
                # far_bias, far_list = center_refresh(far_list, far_center, far_index)

                # the circumscribed circle of triangle
                a = np.sqrt((near_center - medium_center) ** 2 + (car.near_pos - car.medium_pos) ** 2)
                b = np.sqrt((far_center - medium_center) ** 2 + (car.far_pos - car.medium_pos) ** 2)
                c = np.sqrt((far_center - near_center) ** 2 + (car.far_pos - car.near_pos) ** 2)
                p = (a + b + c) / 2
                r = (a * b * c) / (4 * np.sqrt(p * (p - a) * (p - b) * (p - c)))

                # use radius to help car get better control
                if r > 400:
                    if abs(far_center - 320) < 40:
                        car.state = CarState.fast_go
                    elif far_center - 320 > 0:
                        car.state = CarState.light_right
                    else:
                        car.state = CarState.light_left
                elif r < 100:
                    if abs(far_center - 320) < 40:
                        car.state = CarState.go
                    elif far_center - 320 > 200:
                        car.state = CarState.heavy_right
                    elif far_center - 320 > 0:
                        car.state = CarState.right
                    elif far_center - 320 < -200:
                        car.state = CarState.heavy_left
                    elif far_center - 320 < 0:
                        car.state = CarState.left
                else:
                    if abs(far_center - 320) < 40:
                        car.state = CarState.go
                    elif far_center - 320 > 0:
                        car.state = CarState.right
                    else:
                        car.state = CarState.left

            # take control of car
            if car.state == CarState.stop:
                car.brake()
            elif car.state == CarState.go:
                car.forward(30)
            elif car.state == CarState.fast_go:
                car.forward(50)
            elif car.state == CarState.light_left:
                car.left(30)
            elif car.state == CarState.left:
                car.left(50)
            elif car.state == CarState.heavy_left:
                car.left(70)
            elif car.state == CarState.light_right:
                car.right(30)
            elif car.state == CarState.right:
                car.right(50)
            elif car.state == CarState.heavy_right:
                car.right(70)

            rawCapture.truncate(0)  # PiCamera必备

            mfps = 1 / (time.time() - t_start)  # 计算FPS
            print('FPS: ', mfps, 'state: ', car.state)



    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()

    except:
        print("stop")
        car.AllStop()
