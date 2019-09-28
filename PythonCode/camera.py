from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as py
import cv2

class CarCamera(object):
    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        time.sleep(0.1) # time for camera start

    def PhotoTaking(self):  # take a photo     
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array
        # cv2.imshow("Image", image)
        # cv2.waitKey(1000)  # 如果没有该命令，则下次camera无法正常打开
        return image

    def VideoRecording(self):
        return self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

 
if __name__ == '__main__':
    try:
        cam = CarCamera()

        for frame in cam.VideoRecording():
            image = frame.array  # grab the raw NumPy array representing the image, then initialize the timestamp

            # show the frame
            # cv2.imshow("Frame", image)
            print("Image---")
            # 如果没有下列命令，则下次camera无法正常打开
            key = cv2.waitKey(1) & 0xFF # 按下任意按键返回（按下按键时，焦点要在图像窗口上）

            # clear the stream in preparation for the next frame
            cam.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        cv2.waitKey(1)
        cam.rawCapture.truncate(0)
        cv2.destroyAllWindows()



