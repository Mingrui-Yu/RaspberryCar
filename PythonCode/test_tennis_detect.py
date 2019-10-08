import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt

class CarDetect(object):
    def __init__(self):
        self.lower_bound = np.array([10,90, 100])
        self.higher_bound = np.array([50, 200, 255])


    def TennisDetect(self, img):
        img = cv2.blur(img, (5,5))
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # ave_bright = np.mean(hsv_img[:, :, 2])
        # add_bright = 100 - ave_bright
        # hsv_img[:, :, 2][hsv_img[:, :, 2]>=255 - add_bright] =  255
        # hsv_img[:, :, 2][hsv_img[:, :, 2]<255 - add_bright] = hsv_img[:, :, 2][hsv_img[:, :, 2]<255 - add_bright] + add_bright

        # print('brightness: ', np.mean(hsv_img[:, :, 2]))

        (h_img, s_img, v_img) = cv2.split(hsv_img)

        rgb_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

        # mask_img = cv2.inRange(hsv_img, self.lower_bound, self.higher_bound)

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        dst_img = cv2.equalizeHist(gray_img)

        # edge_img = cv2.Canny(gray_img, 30, 100)
        # edge_img_rgb = cv2.cvtColor(edge_img, cv2.COLOR_GRAY2BGR)
        dst_img_rgb = cv2.cvtColor(dst_img, cv2.COLOR_GRAY2BGR)
        
        circles = cv2.HoughCircles(dst_img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=20, minRadius=15, maxRadius=50)
        # print(circles)

        img_out = copy.copy(hsv_img)

        # x = 531
        # y = 337
        # r = 30
        # s_r = int(r/1.5)

        # detect_area = copy.copy(img[y-s_r: y+s_r, x-s_r:x+s_r])
        # hsv_area = cv2.cvtColor(detect_area, cv2.COLOR_BGR2HSV)
        # hist_H = cv2.calcHist([hsv_area], [0], None, [181], [0, 180])
        # hist_S = cv2.calcHist([hsv_area], [1], None, [256], [0, 255])
        # hist_V = cv2.calcHist([hsv_area], [2], None, [256], [0, 255])

        # plt.plot(hist_H), plt.xticks(np.arange(0, 180, 10))
        # plt.show()
        # plt.plot(hist_S), plt.xticks(np.arange(0, 255, 10))
        # plt.show()
        # plt.plot(hist_V), plt.xticks(np.arange(0, 255, 10))
        # plt.show()

        if len(circles):
            x = circles[0][:, 0].astype(int)
            y = circles[0][:, 1].astype(int)
            r = circles[0][:, 2].astype(int)
            s_r = (r/1.5).astype(int)

            num = circles[0].shape[0]
            distance = np.zeros(num)
            mean_h = np.zeros(num)
            mean_s = np.zeros(num)
            mean_v = np.zeros(num)

            for i in range(num):

                detect_area_h = (h_img[y[i]-s_r[i]: y[i]+s_r[i], x[i]-s_r[i]:x[i]+s_r[i]])
                detect_area_s = (s_img[y[i]-s_r[i]: y[i]+s_r[i], x[i]-s_r[i]:x[i]+s_r[i]])
                detect_area_v = (v_img[y[i]-s_r[i]: y[i]+s_r[i], x[i]-s_r[i]:x[i]+s_r[i]])

                mean_h[i] = np.mean(detect_area_h)
                mean_s[i] = np.mean(detect_area_s)
                mean_v[i] = np.mean(detect_area_v)

                distance[i] = np.sqrt(0.98*(mean_h[i] - 36)**2 + 0.02*(mean_s[i] - 163)**2)

                img_out = cv2.circle(img_out, (x[i],y[i]), r[i], (0,255,0), 1, 8, 0)
                
            i = np.argmin(distance)
            img_out = cv2.circle(img_out, (x[i],y[i]), r[i], (0,0,255), 1, 8, 0)
            print('x:',x[i], ' y:', y[i], ' distance:', distance[i], ' mean_h:', mean_h[i], ' mean_s:', mean_s[i], ' mean_v:', mean_v[i])


            
        return img_out, mean_h[i], mean_s[i], mean_v[i]


if __name__ == '__main__':
    try:
        detect = CarDetect()

        correct = [1, 2, 3, 4, 5, 6 ,9 , 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 32]
        mean_h = []
        mean_s = []
        mean_v = []

        for i in correct:

            img = cv2.imread('/home/mingrui/Mingrui/RaspberryCar/photo_tennis/tennis_'+ str(i) +'.jpg')

            img_out, h, s, v = detect.TennisDetect(img)
            cv2.imshow('out'+str(i), img_out)
            cv2.waitKey(0)

            mean_h.append(h)
            mean_s.append(s)
            mean_v.append(v)

        ave_h = np.mean(mean_h)
        var_h = np.var(mean_h)
        print('ave_h:', ave_h, ' var_h:', var_h)

        ave_s = np.mean(mean_s)
        var_s = np.var(mean_s)
        print('ave_s:', ave_s, ' var_s:', var_s)

        ave_v = np.mean(mean_v)
        var_v = np.var(mean_v)
        print('ave_v:', ave_v, ' var_v:', var_v)


    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        
