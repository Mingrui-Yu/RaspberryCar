import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import time
from enum import Enum
import copy

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


if __name__ == '__main__':
    try:
        car = Car()

        VideoReturn = True
        turn_right_speed = 60
        turn_left_speed = 50
        forward_speed = 50
        speed_high = 60
        speed_low = 0

        camera, rawCapture = car.CameraInit()  # Initialize the PiCamera
        for raw_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            t_start = time.time()  # 用来计算FPS

            frame_origin = raw_frame.array


            ################## 车道检测 ##############################################
            img = cv2.blur(frame_origin, (5, 5))  # denoising
            _, _, red_img = cv2.split(img)

            # gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # rgb to gray

            _, dst = cv2.threshold(red_img,  20, 255, cv2.THRESH_BINARY)  # OTSU binaryzation
            # _, dst = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)  # OTSU binaryzation
            #  dst = cv2.dilate(dst, None, iterations=2)  # dilate image to add the white area

            height, width = dst.shape
            half_width = int (width/2)

            right_line_pos = np.zeros((4, 1))
            left_line_pos = np.zeros((4, 1))

            img_out = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)

            for i in range(4):
                detect_height = height - 25 * (i+1)
                detect_area_left = dst[detect_height, 0: half_width - 1]
                detect_area_right = dst[detect_height, half_width: width-1]
                line_left = np.where(detect_area_left == 0)
                line_right = np.where(detect_area_right == 0)

                if len(line_left[0]):
                    left_line_pos[i] = int(np.max(line_left))
                else:
                    left_line_pos[i] = 0

                if len(line_right[0]):
                    right_line_pos[i] = int(np.min(line_right))
                else:
                    right_line_pos[i] = 0               

                if left_line_pos[i]:
                    img_out = cv2.circle(img_out, (left_line_pos[i], detect_height), 4, (0, 0, 255), thickness=10)
                if right_line_pos[i]:
                    img_out = cv2.circle(img_out, (half_width + right_line_pos[i], detect_height), 4, (0, 0, 255), thickness=10)

            if VideoReturn:  # detect the tennis & transmit the frames to PC
                car.VideoTransmission(img_out)


            ############################ 运动控制 #####################################
            if (any(left_line_pos) and any(right_line_pos)):
                ForB = 'Forward'
                LorR = 'Brake'
            elif any(left_line_pos) == 0 and any(right_line_pos) == 0:
                pass
                # ForB = 'Forward'
                # LorR = 'Brake'
            elif any(left_line_pos) == 0:
                if np.min(right_line_pos) < 50:
                    ForB = 'Brake'
                    LorR = 'Left'
                else: 
                    ForB = 'Forward'
                    LorR = 'Left'
            elif any(right_line_pos) == 0:
                if np.max(left_line_pos) > half_width - 50:
                    ForB = 'Brake'
                    LorR = 'Right'
                else: 
                    ForB = 'Forward'
                    LorR = 'Right'


            if ForB is 'Brake':
                if LorR is 'Left':
                    car.left(turn_left_speed)
                    # car.forward_turn(0, speed_high)
                elif LorR is 'Right':
                    car.right(turn_right_speed)
                    # car.forward_turn(speed_high, 0)
                elif LorR is 'Brake':
                    car.brake()
            elif ForB is 'Forward':
                if LorR is 'Left':
                    car.forward_turn(speed_low, speed_high)
                elif LorR is 'Right':
                    car.forward_turn(speed_high, speed_low)
                elif LorR is 'Brake':
                    car.forward(forward_speed)
            elif ForB is 'Backward':
                if LorR is 'Left':
                    car.left(turn_left_speed)
                elif LorR is 'Right':
                    car.right(turn_right_speed)
                elif LorR is 'Brake':
                    car.back(40)






            rawCapture.truncate(0)  # PiCamera必备



    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()

    except:
        print("stop")
        car.AllStop()
