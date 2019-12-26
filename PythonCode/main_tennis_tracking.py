import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared
from camera import CarCamera
from detect_new import CarDetect

GPIO.setwarnings(False)  # Disable warning
GPIO.setmode(GPIO.BCM)  # BCM coding 


class Car(CarMove, CarUltrasound, CarInfrared, CarCamera, CarDetect):  # create class Car, which derives all the modules
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)
        CarCamera.__init__(self)
        CarDetect.__init__(self)
    
    def AllStop(self):
        CarMove.MotorStop(self)
        CarCamera.CameraCleanup(self)
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        car = Car() 

        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # video_out = cv2.VideoWriter('out.mp4', fourcc, 10, (640, 480))

        VideoReturn = True  #  return the detected_frame, and transmit the frames to PC
        radius_mov_ave = 35
        x_mov_ave = 320
        turn_speed = 60

        camera, rawCapture = car.CameraInit()  # Initialize the PiCamera

        for raw_frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
            t_start = time.time()  # 用来计算FPS

            frame_origin = raw_frame.array
            
            if VideoReturn:  # detect the tennis & transmit the frames to PC
                frame_detect, x_pos, y_pos, radius = car.TennisDetect(frame_origin, VideoReturn)
                car.VideoTransmission(frame_detect)
                video_out.write(frame_detect)
            else:
                x_pos, y_pos, radius = car.TennisDetect(frame_origin, VideoReturn)
                # car.VideoTransmission(frame_origin)

            # print('x: ', x_pos ,'  y: ', y_pos, '  r: ', radius)

            if radius == 0:  # radius ==0 means it hasn't found the tennis
                pass
            else:
                radius_mov_ave = 0.4*radius + 0.6*radius_mov_ave  # use the moving average  to reduce the error
                x_mov_ave = 0.4*x_pos + 0.6*x_mov_ave


            ##### decision making #####
            if radius == 0:
                ForB = 'Brake'
            elif radius_mov_ave < 30:
                ForB = 'Forward'
            elif radius_mov_ave > 40:
                ForB = 'Backward'
            else:
                ForB = 'Brake'

            if x_pos == 0:
                LorR = 'Brake'
            elif x_mov_ave > 420: 
                LorR = 'Right'
            elif x_mov_ave < 220: 
                LorR = 'Left'
            else: 
                LorR = 'Brake'

            if ForB is 'Brake':
                if LorR is 'Left':
                    car.left(turn_speed)
                elif LorR is 'Right':
                    car.right(turn_speed)
                elif LorR is 'Brake':
                    car.brake()
            elif ForB is 'Forward':
                if LorR is 'Left':
                    car.left(turn_speed)
                elif LorR is 'Right':
                    car.right(turn_speed)
                elif LorR is 'Brake':
                    car.forward(50)
            elif ForB is 'Backward':
                if LorR is 'Left':
                    car.left(turn_speed)
                elif LorR is 'Right':
                    car.right(turn_speed)
                elif LorR is 'Brake':
                    car.back(40)


            rawCapture.truncate(0)  # PiCamera必备
            
            mfps = 1 / (time.time() - t_start)  # 计算FPS
            print('FPS: ', mfps)
            


    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()
        # video_out.release()