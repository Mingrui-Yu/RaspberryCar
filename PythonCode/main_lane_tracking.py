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
        num_lane_point = 4   # the number of detected points on the lane
        turn_right_speed = 50
        turn_left_speed = 50
        forward_speed = 40
        speed_high = 60
        speed_low = 0

        ForB = 'Forward'
        LorR = 'Brake'

        camera, rawCapture = car.CameraInit()  # Initialize the PiCamera
        for raw_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame_origin = raw_frame.array

            ################## lane detection ##############################################
            img = cv2.blur(frame_origin, (5, 5))  # denoising
            _, _, red_img = cv2.split(img)  # extract the red channel of the RGB image (since the lane in our experiment is blue or black)
            # gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # rgb to gray

            _, dst = cv2.threshold(red_img,  20, 255, cv2.THRESH_BINARY)  # binaryzation, the thresold deponds on the light in the environment

            height, width = dst.shape
            half_width = int (width/2)
            
            right_line_pos = np.zeros((num_lane_point, 1))
            left_line_pos = np.zeros((num_lane_point, 1))

            img_out = cv2.cvtColor(dst, cv2.COLOR_GRAY2RGB)
            for i in range(num_lane_point):   # each detected point on the lane
                detect_height = height - 15 * (i+1)
                detect_area_left = dst[detect_height, 0: half_width - 1]  # divide the image into two parts: left and right (this may cause problems, which can be optimized in the future)
                detect_area_right = dst[detect_height, half_width: width-1]
                line_left = np.where(detect_area_left == 0)   # extract  zero pixels' index
                line_right = np.where(detect_area_right == 0)

                if len(line_left[0]):
                    left_line_pos[i] = int(np.max(line_left))  # set the most internal pixel as the lane point
                else:
                    left_line_pos[i] = 0  # if haven't detected any zero pixel, set the lane point as 0

                if len(line_right[0]):
                    right_line_pos[i] = int(np.min(line_right))
                else:
                    right_line_pos[i] = half_width - 1               

                if left_line_pos[i] != 0:   # draw the lane points on the binary image
                    img_out = cv2.circle(img_out, (left_line_pos[i], detect_height), 4, (0, 0, 255), thickness=10)
                if right_line_pos[i] != half_width - 1:
                    img_out = cv2.circle(img_out, (half_width + right_line_pos[i], detect_height), 4, (0, 0, 255), thickness=10)

            if VideoReturn:  # detect the tennis & transmit the frames to PC
                car.VideoTransmission(img_out)


            ############################ decision making #####################################
            left_max = np.max(left_line_pos)
            right_min = np.min(right_line_pos)  # choose the most internal lane point for decision making

             # if no detected lane, then keep the last action
             #  if only detected the right lane: 
                #  if the right lane is still close to the image border, then go straight; 
                #  if the right lane is too close to the image center, then spin around; 
                #  else, then turn and go straight
            # if only detected the left lane: similar to the above
            # if both lanes is detected: go straight
            if left_max == 0 and right_min == half_width - 1: 
                pass
            elif left_max == 0: 
                if right_min > half_width - 100:  
                    ForB = 'Forward'
                    LorR = 'Brake'
                elif right_min < 100:   
                    ForB = 'Brake'
                    LorR = 'Left'
                else:   
                    ForB = 'Forward'
                    LorR = 'Left'
            elif right_min == half_width - 1:
                if left_max <100:
                    ForB = 'Forward'
                    LorR = 'Brake'
                elif left_max > half_width - 100:
                    ForB = 'Brake'
                    LorR = 'Right'
                else:
                    ForB = 'Forward'
                    LorR = 'Right'
            else:
                ForB = 'Forward'
                LorR = 'Brake'
            
            ############################ motion control #####################################
            if ForB is 'Brake':
                if LorR is 'Left':
                    car.left(turn_left_speed)
                elif LorR is 'Right':
                    car.right(turn_right_speed)
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
