import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class CarRun(object):
    def __init__(self):
        
        GPIO_motor_1 = 18
        GPIO_motor_4 = 23
        GPIO_motor_5 = 24
        GPIO_motor_6 = 25

        GPIO.setup(GPIO_motor_1, GPIO.OUT)
        GPIO.setup(GPIO_motor_4, GPIO.OUT)
        GPIO.setup(GPIO_motor_5, GPIO.OUT)
        GPIO.setup(GPIO_motor_6, GPIO.OUT)

        self.motor_1 = GPIO.PWM(GPIO_motor_1, 500)
        self.motor_4 = GPIO.PWM(GPIO_motor_4, 500)
        self.motor_5 = GPIO.PWM(GPIO_motor_5, 500)
        self.motor_6 = GPIO.PWM(GPIO_motor_6, 500)

    def forward(self, speed):
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)
        self.motor_5.ChangeDutyCycle(speed)
        self.motor_6.ChangeDutyCycle(0)

    def back(self, speed):
        self.motor_1.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(speed)
        self.motor_5.ChangeDutyCycle(0)
        self.motor_6.ChangeDutyCycle(speed)

    def left(self, speed):
        self.motor_1.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(speed)
        self.motor_5.ChangeDutyCycle(speed)
        self.motor_6.ChangeDutyCycle(0)

    def right(self, speed):
        self.motor_1.ChangeDutyCycle(speed)
        self.motor_4.ChangeDutyCycle(0)
        self.motor_5.ChangeDutyCycle(0)
        self.motor_6.ChangeDutyCycle(speed)

    def brake(self):
        self.motor_1.ChangeDutyCycle(0)
        self.motor_4.ChangeDutyCycle(0)
        self.motor_5.ChangeDutyCycle(0)
        self.motor_6.ChangeDutyCycle(0)


if __name__ == '__main__':
    try:
        car = CarRun()
        car.motor_1.start(0)
        car.motor_4.start(0)
        car.motor_5.start(0)
        car.motor_6.start(0)
        while(True):
            car.forward(50)
        motor_1.stop()

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

