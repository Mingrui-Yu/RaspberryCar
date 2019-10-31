# RaspberryCar

An intelligent car based on Raspberry-Pi-3.

（中文介绍请往后翻）

## Platform
Raspberry-Pi-3

L298N

Camera (CSI)

Ultrasonic ranging sensor

Infrared obstacle avoidance sensor

Car (4 motors)

## Environment

### On Raspiberry Pi:

python 3

RPi.GPIO

opencv   [How to install](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/opencv_python.md#%E5%9C%A8%E6%A0%91%E8%8E%93%E6%B4%BE%E4%B8%8A%E5%AE%89%E8%A3%85%E5%9F%BA%E4%BA%8Epython%E7%9A%84opencv)

picamera

tensorflow

TensorFlow Object Detection API

### On PC:

python 3

opencv

## Run

### Obstacle avoidance

Based on ultrasonic sensor and infrared sensors.

Enter the following commands in Pi Terminal:
```
cd PythonCode
python3 main_obstacle_avoidance.py
```
Has been tested.

### Tracking

Based on infrared sensors.

Enter the following commands in Pi Terminal:
```
cd PythonCode
python3 main_trace_test.py
```
循迹传感器可以正常工作，寻迹逻辑还未进行测试

### Video recording & Video transmittion from Pi to PC

Enter the following commands in Pi Terminal:
```
cd PythonCode
python3 camera.py
```
Besides, if you want to watch the video from PC, then enter the following commands in PC Terminal:
```
cd PythonCode
python3 pc_reciever.py
```

Has been tested.

### Tennis Tracking

The car will first detect the tennis based on its camera (finished and tested), then it will move to track the tennis (work in next).

Enter the following commands in Pi Terminal:
```
cd PythonCode
python3 main_tennis_tracking.py
```
Besides, if you want to watch the video with the detected result from PC, then enter the following commands in PC Terminal:
```
cd PythonCode
python3 pc_reciever.py
```

### Object Detection
Based on TensorFLow Object Detection API, using the 'ssdlite_mobilenet_v2_coco_2018_05_09' pre-trained model. 

(相关支持已经上传至树莓派PythonCode文件夹，所以不再上传至此repository)

NOTICE:
相关支持已经上传至树莓派PythonCode文件夹，所以再上传代码的时候小心，不要把相关支持覆盖了。

## Notes
[All tutorials on Raspberry-Pi | GitHub](https://github.com/Mingrui-Yu/Tutorials/tree/master/Rapberry_Pi)

* [创建wifi热点&开启SSH](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E5%88%9B%E5%BB%BAwifi%E7%83%AD%E7%82%B9%26%E5%BC%80%E5%90%AFSSH%26putty%E8%BF%9E%E6%8E%A5.md#pi3-%E5%88%9B%E5%BB%BAwifi%E7%83%AD%E7%82%B9--%E5%BC%80%E5%90%AFssh--putty%E8%BF%9E%E6%8E%A5)

* [相机&opencv-python](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E7%9B%B8%E6%9C%BA%26opencv_python.md#%E5%9C%A8%E6%A0%91%E8%8E%93%E6%B4%BE%E4%B8%8A%E5%AE%89%E8%A3%85%E5%9F%BA%E4%BA%8Epython%E7%9A%84opencv)

* [更换下载源](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E6%9B%B4%E6%8D%A2%E4%B8%8B%E8%BD%BD%E6%BA%90.md#%E5%88%87%E6%8D%A2%E5%88%B0%E5%9B%BD%E5%86%85%E7%9A%84apt-get%E4%B8%8B%E8%BD%BD%E6%BA%90)

* [TensorFlow相关](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E5%AE%89%E8%A3%85tensorflow.md#tensorflow-%E5%AE%89%E8%A3%85)

* [直流电机 & H桥 & PWM](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3.md#%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3%E7%9F%A5%E8%AF%86)

* [超声波传感器相关](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E8%B6%85%E5%A3%B0%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8.md#%E8%B6%85%E5%A3%B0%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8%E7%9B%B8%E5%85%B3)

***

## 简介

本项目是学校项目设计课程内的项目，要求是使用一个基于树莓派的小车来实现一些简单的功能。

目前我们实现的功能有：
* 自动避障：基于超声波和红外，使小车在运行过程中不会撞上障碍物；
* 实时图像传输：将树莓派摄像头拍摄到的视频流传到PC端，并在PC端查看；
* 目标检测：识别并定位摄像头图像中的各类常见物体；
* 网球追踪：基于摄像头，使小车追踪一个移动的网球，并与网球保持一定距离。

学校提供的小车的商家是[慧净电子](http://www.hlmcu.com/)，商家提供了一些使用教程，适合初学，基于C语言，实现了一些简单的红外避障、红外寻迹、超声波避障和摄像头调用。

本项目选用Python作为编程语言，有几点原因：Python相比较C语言更简明；我们对Python的掌握情况更好一些（C语言没学好啊）；方便之后使用tensorflow做一些深度学习的功能。但同时带来的缺点就是运行速度会差一点。

下面我们会对小车配置、功能实现和使用方法进行详细的介绍。

### 整体架构

我们的源代码全部放在PythonCode文件夹内。

我们对每个传感器定义了一个类，放在相应的py文件里，由此可以很清晰方便地对每个传感器进行单独的调试。

名称以main开头的文件是实现相应功能的主程序，在主程序里定义了一个Car类，该类继承了所有传感器的类。

## 准备工作

### 重装树莓派的系统

商家给树莓派预装了系统，应该是商家自己改过的，也是几年前的了。强烈建议自己将树莓派的系统进行重装（重装后opencv和tensorflow的安装都会简单很多），推荐安装树莓派的官方系统[Raspbian](https://www.raspberrypi.org/downloads/raspbian/)。安装方法百度一下，教程很多，也很简单。

关于树莓派教程，推荐[树莓派实验室|开箱上手必读](http://shumeipai.nxez.com/hot-explorer#beginner)，里面的教程基本准确好用。

### 使用SSH登录，操作树莓派
对树莓派进行操作的方法有很多：
* [连接鼠标键盘](http://shumeipai.nxez.com/2013/09/07/how-to-install-and-activate-raspberry-pi.html)
* [使用远程桌面](http://shumeipai.nxez.com/2018/08/31/raspberry-pi-vnc-viewer-configuration-tutorial.html)
* [使用PuTTY登录到树莓派](http://shumeipai.nxez.com/2013/09/07/using-putty-to-log-in-to-the-raspberry-pie.html)

我们基本上是使用SSH登录到树莓派进行操作的，也就是使用putty登录。这需要树莓派和PC在同一个局域网下，我们选择让树莓派创建一个WiFi热点，然后让PC连接这个WiFi热点。方法：[创建WiFi热点并开机自启动](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E5%88%9B%E5%BB%BAwifi%E7%83%AD%E7%82%B9%26%E5%BC%80%E5%90%AFSSH%26putty%E8%BF%9E%E6%8E%A5.md#pi3-%E5%88%9B%E5%BB%BAwifi%E7%83%AD%E7%82%B9--%E5%BC%80%E5%90%AFssh--putty%E8%BF%9E%E6%8E%A5)，其中使用了github上一个开源的库create_ap。同时，还要设置热点开机自动启动。另外注意要设置[开启树莓派的SSH服务](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E5%88%9B%E5%BB%BAwifi%E7%83%AD%E7%82%B9%26%E5%BC%80%E5%90%AFSSH%26putty%E8%BF%9E%E6%8E%A5.md#%E5%BC%80%E5%90%AFssh%E6%9C%8D%E5%8A%A1)，否则putty连接会显示失败。

### 更换下载源
使用官方的源因为众所周知的原因会非常慢且不稳定，所以要换成国内的源。
* [更换apt源](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E6%9B%B4%E6%8D%A2%E4%B8%8B%E8%BD%BD%E6%BA%90.md#%E5%88%87%E6%8D%A2%E5%88%B0%E5%9B%BD%E5%86%85%E7%9A%84apt-get%E4%B8%8B%E8%BD%BD%E6%BA%90)
* [更换pip源](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E6%9B%B4%E6%8D%A2%E4%B8%8B%E8%BD%BD%E6%BA%90.md#%E5%88%87%E6%8D%A2%E5%88%B0%E5%9B%BD%E5%86%85%E7%9A%84pippip3%E4%B8%8B%E8%BD%BD%E6%BA%90)

### OpenCV安装
使用最新版树莓派系统，可以直接用pip3安装OpenCV。

教程：[python3 + opencv](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E7%9B%B8%E6%9C%BA%26opencv_python.md#python3--opencv)

## 硬件调试

### 电机
[直流电机相关知识](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3.md#%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3%E7%9F%A5%E8%AF%86)
* 工作原理
* H桥
* PWM

电机相关代码在move.py内。需要注意GPIO端口号的设置，python用的是BCM编码。

![树莓派GPIO编号图](https://github.com/Mingrui-Yu/PicturesGitHub/raw/master/RaspberryCar/GPIO.png)

在move.py中，定义了前进、后退、左转、右转、停车功能。转弯是通过左右轮差速实现的。

### 超声波测距传感器
[超声波测距传感器有关知识](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E8%B6%85%E5%A3%B0%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8.md#%E8%B6%85%E5%A3%B0%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8%E7%9B%B8%E5%85%B3)
* 超声波测距基本原理
* 超声波测距程序实现
* 提升测距准确性的方法
  
超声波相关代码在ultrasound.py内，实现了超声波测距和对测距进行移动平均来减小误差。

### 红外避障传感器
红外避障相关代码在infrared.py内，InfraredMeasure函数是小车左右的两个红外避障传感器，TrackingMeasure是小车底部两个红外寻线传感器。

注意，红外避障传感器传回0表示前方有障碍物，传回1表示前方无障碍物。

### 摄像头

调用摄像头需要先在```在 sudo raspi-config```中启用Camera，然后重启。

python调用摄像头有两种方式：
* 使用picamera
* 使用opencv

我们使用的是picamera方式，因为我们发现使用OpenCV的方式会有延时，它返回的第一帧图像是在镜头初始化那一刻的图像，而不是主程序请求时的图像。

具体调用方法参考 [树莓派（Raspberry Pi）中PiCamera+OpenCV的使用](https://blog.csdn.net/u012005313/article/details/70244747#C0)。

摄像头相关代码在camera.py中，其中实现了：
* 摄像头初始化
* 实时图像传输（发送端），注意HOST为PC在此WiFi网络下的IP地址（通过ifconfig查看），PORT设置一个和接收端相同的端口号就可以。

另外注意，程序终止是一定要关闭摄像机（camera.close()），否则下次无法正常打开。


## 功能实现

### 自动避障

基于超声波和红外，使小车在运行过程中不会撞上障碍物。

主程序为main_obstacle_avoidance.py，其思想很简单，超声波传感器测出小车距离前方障碍物的距离，两边的红外传感器测出两边是否有障碍物，根据测量结果进行运动决策和电机控制。

### 实时图像传输
将树莓派摄像头拍摄到的视频流传到PC端，并在PC端查看。目的是为了便于摄像头姿态的调整和图像处理算法的调试。另外，如果需要的话可以使用传输到PC的图像在PC端进行处理（我们没有实现此功能）。

可选择的传输协议有两种：
* TCP：面向连接，提供可靠地服务，无差错，不丢失，不重复；实时性差，效率低；系统资源要求较多。
* UDP：可以无连接；尽最大努力交付，即不保证可靠交付；实时性强，效率高；系统资源要求较少。

我们使用UDP传输协议进行图像传输。具体实现主要分为发送端和接收端两部分
：
* 发送端：(camera.py VideoTransimssion)
  * 图像编码（cv2.imencode）
  * 校验数据发送（数据长度作为校验）
  * 编码数据发送（socket.sendall）
* 接收端：(pc_receiver.py)
  * 接收校验数据（4字节数据）
  * 接收图像编码（校验数据后的第一个数据包）
  * 简单校验（校验数据 == 编码数据长度）
  * 图像解码（cv2.imdecode）
其中，发送端在树莓派端运行，接收端在PC端运行。二者同时运行。

### 目标检测

识别并定位摄像头图像中的各类常见物体。

主程序为main_object_detection.py，其调用了TensorFlow Object Detection API，使用了训练好的的SSDLite目标检测模型，在树莓派端进行目标检测
。

![目标检测效果](https://github.com/Mingrui-Yu/PicturesGitHub/raw/master/RaspberryCar/object_detection.gif)
