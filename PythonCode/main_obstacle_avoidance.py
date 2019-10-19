import RPi.GPIO as GPIO
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

from move import CarMove
from ultrasound import CarUltrasound
from infrared import CarInfrared
from camera import CarCamera

GPIO.setwarnings(False)  # Disable warning
GPIO.setmode(GPIO.BCM)  # BCM coding 

class Car(CarMove, CarUltrasound, CarInfrared, CarCamera):  # create class Car, which derives all the modules
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)
        CarCamera.__init__(self)
    
    def AllStop(self):
        CarMove.MotorStop(self)
        CarCamera.CameraCleanup(self)
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        car = Car() 
        start_time = None

        while True:
            # perception
            dist_mov_ave = car.DistMeasureMovingAverage()
            print('Distance', dist_mov_ave)

            [left_measure, right_measure] = car.InfraredMeasure()

            # decison-making
            if (start_time is None) or (time.time() - start_time >  0.5):
                start_time = None
                if left_measure == 0 and right_measure == 1:
                    print("Going right")
                    car.right(80)
                elif left_measure == 1 and right_measure == 0:
                    print("Going left")
                    car.left(80)
                elif left_measure == 0 and right_measure == 0:
                    print("Going back")
                    car.back(50)
                else:
                    if dist_mov_ave < 20:
                        car.left(80)
                        print("Going left")
                        start_time = time.time()
                    elif dist_mov_ave < 100:
                        car.forward(dist_mov_ave/2 + 40)
                    else:
                        car.forward(90)
            else:
                pass




    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()