
import RPi.GPIO as GPIO
import time
  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


  
class CarUltrasound(object):
    def __init__(self):

        self.GPIO_TRIGGER = 20
        self.GPIO_ECHO = 21

        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
  
    def disMeasure(self):
        GPIO.output(self.GPIO_TRIGGER, False)
        time.sleep(0.000002)
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        while GPIO.input(self.GPIO_ECHO) == 0:
            pass
        start_time = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            pass
        stop_time = time.time()
    
        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2
    
        return distance
  

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