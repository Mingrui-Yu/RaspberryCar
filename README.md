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

(picamera)

### On PC:

python 3

opencv

## Run

### Obstacle avoidance

Based on ultrasonic sensor and infrared sensors.

Enter the following commands in Pi Terminal:
```
sudo python3 ./PythonCode/main_obstacle_avoidance.py
```
Has been tested.

### Tracking

Based on infrared sensors.

Enter the following commands in Pi Terminal:
```
sudo python3 ./PythonCode/main_trace_test.py
```
循迹传感器可以正常工作，寻迹逻辑还未进行测试

### Video recording & Video transmittion from Pi to PC

Enter the following commands in Pi Terminal:
```
sudo python3 ./PythonCode/camera.py
```
Besides, if you want to watch the video from PC, then enter the following commands in PC Terminal:
```
sudo python3 ./PythonCode/pc_reciever.py
```

Has been tested.

### Tennis Tracing

The car will first detect the tennis based on its camera (finished and tested), then it will move to trace the tennis (work in next).

Enter the following commands in Pi Terminal:
```
sudo python3 ./PythonCode/main_tennis_tracing.py
```
Besides, if you want to watch the video with the detected result from PC, then enter the following commands in PC Terminal:
```
sudo python3 ./PythonCode/pc_reciever.py
```
## Notes

[直流电机 & H桥 & PWM](https://github.com/Mingrui-Yu/Tutorials/blob/master/Rapberry_Pi/%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3.md#%E7%9B%B4%E6%B5%81%E7%94%B5%E6%9C%BA%E7%9B%B8%E5%85%B3%E7%9F%A5%E8%AF%86)
