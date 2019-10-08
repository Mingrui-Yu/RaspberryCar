import RPi.GPIO as GPIO
import time

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared
from camera import CarCamera
from detect import CarDetect

GPIO.setwarnings(False)  # Disable warning
GPIO.setmode(GPIO.BCM)  # BCM coding 


class Car(CarMove, CarUltrasound, CarInfrared, CarCamera, CarDetect):  # create class Car, which derives all the modules
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)
        CarCamera.__init__(self)
        CarDetect.__init__(self)


if __name__ == '__main__':
    try:
        car = Car() 

        VideoReturn = True
        dist_list = []
        i_frame = 0

        car.brake()

        while True:
            i_frame = i_frame + 1

            ##### perception ######
            # ultrasonic sensing
            dist = car.disMeasure()
            dist_list.append(dist)
            if len(dist_list) > 5:  dist_list.pop(0)
            dist_ave = sum(dist_list)/len(dist_list)  # For error reduction, using the moving average of distance measured by ultrasonic module 
            # print('Distance', dist_ave)

            # infrared sensing
            [left_measure, right_measure] = car.InfraredMeasure()

            # camera sensing
            frame_origin = car.VideoRecording()
            
            if VideoReturn:  # detect the tennis & transmit the frames to PC
                frame_detect, x_pos, y_pos, radius = car.TennisDetect(frame_origin, VideoReturn)
                car.VideoTransmission(frame_detect)
            else:
                x_pos, y_pos, radius = car.TennisDetect(frame_origin, VideoReturn)
                car.VideoTransmission(frame_origin)

            print('x:', x_pos, ' y:', y_pos, ' r:', radius)


            

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        car.CameraCleanup()