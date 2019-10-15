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
    
    def AllStop(self):
        CarMove.MotorStop(self)
        CarCamera.CameraCleanup(self)
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        car = Car() 

        VideoReturn = True
        dist_list = []
        tennis_pos = []
        i_frame = 0

        car.brake()

        while True:
            i_frame = i_frame + 1

            ##### perception ######

            # camera sensing
            frame_origin = car.VideoRecording()
            
            if VideoReturn:  # detect the tennis & transmit the frames to PC
                frame_detect, x_pos, y_pos, radius = car.TennisDetect(frame_origin, VideoReturn)
                car.VideoTransmission(frame_detect)
            else:
                x_pos, y_pos, radius = car.TennisDetect(frame_origin, VideoReturn)
                # car.VideoTransmission(frame_origin)

            print('frame:', i_frame, ' x:', x_pos, ' y:', y_pos, ' r:', radius)

            # if radius == 0:
            #     car.brake()
            # elif radius < 30:
            #     car.forward(30)
            # elif radius > 50:
            #     car.back(30)
            # else:
            #     car.brake()


            # #### under testing ####
            # tennis_pos.append(x_pos)
            # if len(tennis_pos) > 5:  dist_list.pop(0)

            # if x_pos == 0:
            #     car.brake()
            # elif x_pos > 420:
            #     car.right(60)
            # elif x_pos < 220:
            #     car.left(60)
            # else:
            #     car.brake()
            # #### under testing ####


    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()