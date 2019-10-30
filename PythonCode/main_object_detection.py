import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import os

from picamera.array import PiRGBArray
from picamera import PiCamera

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_utils

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

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_out = cv2.VideoWriter('out.mp4', fourcc, 0.8, (640, 480))

        ##### Prepare for the tensorflow object detection API  #####
        MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'  # 使用的模型
        PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'   
        PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt') 
        NUM_CLASSES = 90 
        fileAlreadyExists = os.path.isfile(PATH_TO_CKPT) 

        if not fileAlreadyExists:
            print('Model does not exsist !')
            exit

        print('Loading...')   # Loading the model
        detection_graph = tf.Graph() 
        with detection_graph.as_default(): 
            od_graph_def = tf.GraphDef() 
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid: 
                serialized_graph = fid.read() 
                od_graph_def.ParseFromString(serialized_graph) 
                tf.import_graph_def(od_graph_def, name='')
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS) 
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True) 
        category_index = label_map_util.create_category_index(categories)
        print('Finish Load Graph')

        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0') 
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0') 
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0') 
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0') 
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        ##### Finish the Preparation for the tensorflow object detection API  #####


        ##### Use the Detection Graph #####
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
                camera, rawCapture = car.CameraInit()  # Initialize the PiCamera
                # PiCamera 视频流：
                for raw_frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
                    t_start = time.time()  # 用来计算FPS

                    frame = np.copy(raw_frame.array)
                    frame.setflags(write=1)
                    image_np_expanded = np.expand_dims(frame, axis=0) 
                    
                    print('Running detection..') 
                    (boxes, scores, classes, num) = sess.run( 
                        [detection_boxes, detection_scores, detection_classes, num_detections], 
                        feed_dict={image_tensor: image_np_expanded})   # 使用API来Detect
                    
                    print('Done.  Visualizing..') 
                    vis_utils.visualize_boxes_and_labels_on_image_array(
                            frame,
                            np.squeeze(boxes),
                            np.squeeze(classes).astype(np.int32),
                            np.squeeze(scores),
                            category_index,
                            use_normalized_coordinates=True,
                            line_thickness=8)   # 在frame上画框（检测结果）

                    car.VideoTransmission(frame)  # 向PC传输视频帧
                    video_out.write(frame)


                    rawCapture.truncate(0)  # PiCamera必备

                    mfps = 1 / (time.time() - t_start)  # 计算FPS
                    print('FPS: ', mfps)
            

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.AllStop()
        video_out.release()