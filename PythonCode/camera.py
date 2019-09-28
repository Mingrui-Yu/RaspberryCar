import time
import numpy as py
import cv2
import socket
import struct

class CarCamera(object):
    def __init__(self):
        # initialize the camera and grab a reference to the raw camera capture

        HOST = '192.168.12.60'  # ip of PC
        PORT = 8000  # 随便设置一个，对应起来就行
        self.server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server.connect((HOST,PORT))

        self.capture = cv2.VideoCapture(0)
    

    def VideoRecording(self): 
        success, frame = self.capture.read()

        while not success and frame is None:
                success,frame = self.capture.read()  #获取视频帧
                print('fail to capture image')
        
        return frame


    def VideoTransmission(self, frame):  # transmit video from Pi to PC
        result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY,50])  #编码
        try:
            self.server.sendall(struct.pack('i',imgencode.shape[0]))  # 发送数据长度作为校验
            self.server.sendall(imgencode)
            print("have sent one frame")
        except:
            print("fail to send the frame")


    def CameraCleanup(self):
        self.server.sendall(struct.pack('c',1)) #发送关闭消息
        self.capture.release()
        self.server.close()


if __name__ == '__main__':
    try:
        cam = CarCamera()

        while True:
            frame = cam.VideoRecording()
            cam.VideoTransmission(frame)


    except KeyboardInterrupt:
        cam.CameraCleanup()



