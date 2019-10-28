import cv2
import numpy as np
import copy
import time
import pdb


class CarDetect(object):
    def __init__(self):
        self.track_length = 20
        self.near_pos = 450
        self.medium_pos = 400
        self.far_pos = 360
        pass

    def getcenter(self, line):
        count = np.sum(line == 0)
        index = np.where(line == 0)
        if index == 0:
            index = 1
        try:  # black_index may be none
            center = (index[0][count - 1] + index[0][0]) / 2
        except:
            center = -1
        return center

    def LineTrack(self, img, VideoReturn):  # 检测黑线（利用大津法进行二值化）
        x_bias = 0  # initialize the bias

        img = cv2.blur(img, (5, 5))  # denoising
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # rgb to gray

        _, dst = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU)  # OTSU binaryzation
        dst = cv2.dilate(dst, None, iterations=5)  # dilate image to add the white area
        # dst = cv2.erode(dst, None, iterations=6)
        near_line = dst[self.near_pos]
        medium_line = dst[self.medium_pos]
        far_line = dst[self.far_pos]
        near_center = self.getcenter(self, near_line)
        medium_center = self.getcenter(self, medium_line)
        far_center = self.getcenter(self, far_line)

        if VideoReturn:  # if it needs to return the frame with the detected tennis
            img_out = copy.copy(img)
            img_out = cv2.circle(img_out, (int(near_center), self.near_pos), 4, (0, 0, 255), thickness=10)
            img_out = cv2.circle(img_out, (int(medium_center), self.medium_pos), 4, (0, 0, 255), thickness=10)
            img_out = cv2.circle(img_out, (int(far_center), self.far_pos), 4, (0, 0, 255), thickness=10)
            return img_out, near_center, medium_center, far_center
        else:  # if it only needs to return the position of the detected tennis
            return near_center, medium_center, far_center
