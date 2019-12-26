import cv2
import numpy
import socket
import struct
import copy
import numpy as np



HOST='192.168.12.90'
PORT= 8000
buffSize=65535

if __name__=='__main__':
    server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #创建socket对象
    server.bind((HOST,PORT))
    print('now waiting for frames...')
    i = 7

    while True:
        data,address=server.recvfrom(buffSize) #先接收的是字节长度
        if len(data)==1 and data[0]==1: #如果收到关闭消息则停止程序
            server.close()
            cv2.destroyAllWindows()
            exit()
        if len(data)!=4: #进行简单的校验，长度值是int类型，占四个字节
            length=0
            continue
        else:
            length=struct.unpack('i',data)[0] #长度值
        data,address=server.recvfrom(buffSize) #接收编码图像数据
        if length!=len(data): #进行简单的校验
            print("check error")
            continue
        data=numpy.array(bytearray(data)) #格式转换
        imgdecode=cv2.imdecode(data,1) #解码
        print('have received frame')

        cv2.imshow('frames',imgdecode) #窗口显示

        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite('/home/mingrui/Mingrui/RaspberryCar/photo_tennis/tennis_'+ str(i) +'.jpg', imgdecode)
            i = i + 1


        if cv2.waitKey(1)==27: #按下“ESC”退出
            break

    server.close()
    cv2.destroyAllWindows()

