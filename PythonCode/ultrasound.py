#  Ultrasonic ranging module

import RPi.GPIO as GPIO
import time
  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

  
class CarUltrasound(object):
    def __init__(self):

        self.GPIO_TRIGGER = 20  # GPIO setting (BCM coding)
        self.GPIO_ECHO = 21

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # GPIO input/output definiation
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        self.dist_mov_ave = 0
  
    def DistMeasure(self):  # distance measuing 
        GPIO.output(self.GPIO_TRIGGER, False) 
        time.sleep(0.000002)
        GPIO.output(self.GPIO_TRIGGER, True)  # emit ultrasonic pulse
        time.sleep(0.00001)                   # last 10ms
        GPIO.output(self.GPIO_TRIGGER, False) # end the pulse
        ii = 0

        while GPIO.input(self.GPIO_ECHO) == 0:  # when the pulse is emitted, ECHO will become 1
            ii = ii + 1
            if ii > 1000: 
                print('Ultrasound error 1: the pulse has been emitted, but Echo has not become 1')
                return 0
            pass
        start_time = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:  # when it receives the echo, ECHO will become 0
            current_time = time.time()
            if current_time - start_time > 0.3:
                print('Ultrasound error 2: the sensor missed the echo')
                break
            else:
                pass
        stop_time = time.time()
    
        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2
    
        return distance

    def DistMeasureMovingAverage(self):
        dist_current = self.DistMeasure()
        self.dist_mov_ave = 0.1*dist_current + 0.9*self.dist_mov_ave
        return self.dist_mov_ave

  

if __name__ == '__main__':
    try:
        car = CarUltrasound()
        while True:
            dist = car.disMeasure()
            print("Measured Distance = {:.2f} cm".format(dist))
            time.sleep(1)
  
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()