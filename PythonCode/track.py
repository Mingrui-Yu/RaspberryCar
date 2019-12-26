import cv2
import numpy as np
import copy
import time


class CarDetect(object):
    def __init__(self):
        self.track_length = 20
        self.near_pos = 400
        self.medium_pos = 300
        self.far_pos = 200
        pass

    def group_consecutives(self, vals, step=1):
        run = []
        result = []
        expect = None
        for v in vals[0]:
            if expect is None or abs(v - expect) < 2:
                run.append(v)
            else:
                result.append(run)
                run = []
            expect = v + step
        if result != []:
            print(len(result[0]))
        return result
        # return [vals[0]]

    def denoise(self, areas, pos):
        result = []
        for a in areas:
            if pos == 'near' and abs(len(a) - 125) < 15:
                result.append(a)
            elif pos == 'medium' and abs(len(a) - 90) < 15:
                result.append(a)
            elif pos == 'far' and abs(len(a) - 75) < 15:
                result.append(a)
        print(result)
        return result
        # return areas

    def get_center(self, line):
        if len(line) == 0:
            center = -1
        elif len(line) == 1:
            count = len(line[0])
            index = line
            center = (index[0][count - 1] + index[0][0]) / 2
        else:
            print(len(line))
            center = -1
        return center

    def get_center(self, line):
        index = np.where(line == 255)
        if index == 0:
            index = 1
        sum = np.sum(line == 255)
        if sum > 0:
            center = (index[0][sum - 1] + index[0][0]) / 2
        else:
            center = -1
        return center

    def LineTrack(self, img, VideoReturn):  # 检测黑线（利用大津法进行二值化）
        x_bias = 0  # initialize the bias

        img = cv2.blur(img, (5, 5))  # denoising
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # rgb to gray

        _, dst = cv2.threshold(gray_img, 70, 255, cv2.THRESH_BINARY)  # OTSU binaryzation
        dst = cv2.dilate(dst, None, iterations=2)  # dilate image to add the white area
        # dst = cv2.erode(dst, None, iterations=6)

        near_line = self.group_consecutives(np.where(dst[self.near_pos] == 0))
        medium_line = self.group_consecutives(np.where(dst[self.medium_pos] == 0))
        far_line = self.group_consecutives(np.where(dst[self.far_pos] == 0))

        near_line = self.denoise(near_line, 'near')
        medium_line = self.denoise(medium_line, 'medium')
        far_line = self.denoise(far_line, 'far')

        near_center = self.get_center(near_line)
        medium_center = self.get_center(medium_line)
        far_center = self.get_center(far_line)

        if VideoReturn:  # if it needs to return the frame with the detected tennis
            img_out = copy.copy(dst)
            img_out = cv2.circle(img_out, (int(near_center), self.near_pos), 4, (0, 0, 255), thickness=10)
            img_out = cv2.circle(img_out, (int(medium_center), self.medium_pos), 4, (0, 0, 255), thickness=10)
            img_out = cv2.circle(img_out, (int(far_center), self.far_pos), 4, (0, 0, 255), thickness=10)
            return img_out, near_center, medium_center, far_center
        else:  # if it only needs to return the position of the detected tennis
            return near_center, medium_center, far_center
