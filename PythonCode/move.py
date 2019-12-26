# Car's movement control (forward, back, left, right, brake)
# motor control

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class CarMove(object):
    def __init__(self):
        GPIO_motor_1 = 18  # GPIO setting (BCM coding)
        GPIO_motor_4 = 23
        GPIO_motor_5 = 24
        GPIO_motor_6 = 25

        GPIO.setup(GPIO_motor_1, GPIO.OUT)  # GPIO input/output definiation
        GPIO.setup(GPIO_motor_4, GPIO.OUT)
        GPIO.setup(GPIO_motor_5, GPIO.OUT)
        GPIO.setup(GPIO_motor_6, GPIO.OUT)

        self.motor_1 = GPIO.PWM(GPIO_motor_1, 500)  # PWM initialization: 500 Hz
        self.motor_4 = GPIO.PWM(GPIO_motor_4, 500)
        self.motor_5 = GPIO.PWM(GPIO_motor_5, 500)
        self.motor_6 = GPIO.PWM(GPIO_motor_6, 500)

        self.motor_1.start(0)  # motors start
        self.motor_4.start(0)
        self.motor_5.start(0)
        self.motor_6.start(0)

    def forward(self, speed):
        self.motor_1.ChangeDutyCycle(speed)  # set the duty circle (range: 0~100)
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

    def forward_turn(self, speed_left, speed_right):
        self.motor_1.ChangeDutyCycle(speed_left)
        self.motor_4.ChangeDutyCycle(0)
        self.motor_5.ChangeDutyCycle(speed_right)
        self.motor_6.ChangeDutyCycle(0)

    def MotorStop(self):
        self.motor_1.stop()
        self.motor_4.stop()
        self.motor_5.stop()
        self.motor_6.stop()

    def track_move_left(self, speed, diff):
        self.motor_1.ChangeDutyCycle(40)
        self.motor_4.ChangeDutyCycle(20)
        self.motor_5.ChangeDutyCycle(20)
        self.motor_6.ChangeDutyCycle(40)


if __name__ == '__main__':
    try:
        car = CarMove()
        while (True):
            car.track_move_left(40,10)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.MotorStop()
        GPIO.cleanup()
