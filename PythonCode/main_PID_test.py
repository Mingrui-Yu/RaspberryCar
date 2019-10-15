import RPi.GPIO as GPIO
import time
import math

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared
from camera import CarCamera
from detect import CarDetect
from PID_controller import PID

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
        pid = PID(kp=1, ki=0.0, kd=0.1)
        pid.SetExpectedOutput(15)

        dist_list = []
        min_speed = 30
        FORWARD = True

        while True:

            ##### perception ######
            # ultrasonic sensing
            dist_mov_ave = car.DistMeasureMovingAverage()
            
            motor_speed = - pid.UpdateOutput(dist_mov_ave)

            if motor_speed >= 0:
                FORWARD = True
            else:
                FORWARD = False

            motor_speed = min_speed + min(abs(motor_speed), 100 - min_speed)
            if motor_speed < min_speed + 1:
                motor_speed = 0
            
            if FORWARD:
                car.forward(motor_speed)
            else:
                car.back(motor_speed)

            print('Distance: ', dist_mov_ave, '  Forward: ', FORWARD,  '   Speed: ', motor_speed)







    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()