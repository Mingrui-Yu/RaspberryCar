# RaspberryCar

An intelligent car based on Raspberry-Pi-3.

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

[直流电机 & H桥 & PWM](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3.md#%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3%E7%9F%A5%E8%AF%86)

[超声波传感器相关](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E8%B6%85%E5%A3%B0%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8.md#%E8%B6%85%E5%A3%B0%E6%B3%A2%E4%BC%A0%E6%84%9F%E5%99%A8%E7%9B%B8%E5%85%B3)
