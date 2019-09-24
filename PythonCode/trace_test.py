import RPi.GPIO as GPIO
import time
from run import CarRun
from infrared import CarInfrared
from enum import Enum

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Car(CarRun, CarInfrared):
    def __init__(self):
        CarRun.__init__(self)
        CarInfrared.__init__(self)

class STATUS(Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT=3
    BACK=4

if __name__ == '__main__':
    try:
        car = Car()
        car.motor_1.start(0)
        car.motor_4.start(0)
        car.motor_5.start(0)
        car.motor_6.start(0)

        status = STATUS.STRAIGHT
        
        while True:

            [left_measure, right_measure] = car.TrackingMreasure()

            
            if left_measure == 1 and right_measure == 0:
                print("Going right")
                car.right(80)
                status=STATUS.RIGHT
            elif left_measure == 0 and right_measure == 1:
                print("Going left")
                car.left(80)
                status=STATUS.LEFT
            elif left_measure == 1 and right_measure == 1:
                print("Going straight")
                car.forward(50)
                status=STATUS.RIGHT
            else:
                if status==STATUS.STRAIGHT:
                    car.forward(50)
                elif status==STATUS.RIGHT:
                    car.right(80)
                elif status==STATUS.LEFT:
                    car.left(80)



    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()