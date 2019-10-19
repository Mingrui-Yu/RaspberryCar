import time
import numpy as np
import cv2
import socket
import struct
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

class CarCamera(object):
    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture

        HOST = '192.168.12.90'  # ip of PC
        PORT = 8000  # 随便设置一个，对应起来就行
        self.server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.connect((HOST,PORT))

    
    def CameraInit(self):  # 初始化PiCamera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        rawCapture = PiRGBArray(self.camera, size=(640, 480))
        rawCapture.truncate(0)
        time.sleep(2) # wait for camera starting 相机需要时间预热

        return self.camera, rawCapture


    def VideoTransmission(self, frame):  # transmit video from Pi to PC
        result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 10])  #编码
        try:
            self.server.sendall(struct.pack('i',imgencode.shape[0]))  # 发送数据长度作为校验
            self.server.sendall(imgencode)
            print("have sent one frame")
        except:
            print("fail to send the frame")


    def CameraCleanup(self):
        self.server.sendall(struct.pack('c',1)) #发送关闭消息
        self.server.close()
        self.camera.close()


if __name__ == '__main__':
    try:
        car = CarCamera()
        camera, rawCapture = car.CameraInit()

        for raw_frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
            frame = np.copy(raw_frame.array)

            car.VideoTransmission(frame)  # 向PC传输视频帧

            rawCapture.truncate(0)  # 每一帧结束必须执行此命令，否则无法进行下一帧

    except KeyboardInterrupt:
        car.CameraCleanup()



