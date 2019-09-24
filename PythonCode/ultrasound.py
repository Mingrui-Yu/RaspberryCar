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
  
    def disMeasure(self):  # distance measuing 
        GPIO.output(self.GPIO_TRIGGER, False) 
        time.sleep(0.000002)
        GPIO.output(self.GPIO_TRIGGER, True)  # emit ultrasonic pulse
        time.sleep(0.00001)                   # last 10ms
        GPIO.output(self.GPIO_TRIGGER, False) # end the pulse

        while GPIO.input(self.GPIO_ECHO) == 0:  # when the pulse is emitted, ECHO will become 1
            pass
        start_time = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:  # when it receives the echo, ECHO will become 0
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