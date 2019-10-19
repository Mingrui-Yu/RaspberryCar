import cv2
import numpy as np
import copy

class CarDetect(object):
    def __init__(self):
        pass


    def TennisDetect(self, img, VideoReturn):   # 检测网球（利用霍夫圆检测和HSV色彩检测）
        x_pos = 0  # initialize the tennis's position
        y_pos = 0
        radius = 0

        img = cv2.blur(img, (5,5))  # denoising
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # rgb to HSV
        (h_img, s_img, v_img) = cv2.split(hsv_img)

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # rgb to gray
        dst_img = cv2.equalizeHist(gray_img)  # hist equalization

        circles = cv2.HoughCircles(dst_img, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=20, minRadius=15, maxRadius=50)  # HOUGH circle detection

        if circles is not None:  
            x = circles[0][:, 0].astype(int)  # extract the x, y, r of all detected circles
            y = circles[0][:, 1].astype(int)
            r = circles[0][:, 2].astype(int)
            s_r = (r/1.5).astype(int)  

            num = circles[0].shape[0]
            distance = np.zeros(num)
            mean_h = np.zeros(num)
            mean_s = np.zeros(num)

            for i in range(num):  # traverse all detected circles:
                detect_area_h = (h_img[y[i]-s_r[i]: y[i]+s_r[i], x[i]-s_r[i]:x[i]+s_r[i]])  # A square in the detected circle (H)
                detect_area_s = (s_img[y[i]-s_r[i]: y[i]+s_r[i], x[i]-s_r[i]:x[i]+s_r[i]])  # A square in the detected circle (S)

                mean_h[i] = np.mean(detect_area_h)
                mean_s[i] = np.mean(detect_area_s)

                # Through 33 photos of the tennis captured by Raspberry Camera, we find the average H of tennis areas is 36, the average S of tennis areas is 163, and the var of H is much smaller than that of S.
                distance[i] = np.sqrt(0.98*(mean_h[i] - 36)**2 + 0.02*(mean_s[i] - 163)**2) 
                
            i = np.argmin(distance)  # select the circle with the minimum distance as the detected tennis
            if distance[i] < 15:   # if distance > 15, the selected circle cannot be a tennis
                SuccessfulDetect = True
                x_pos = x[i]
                y_pos = y[i]
                radius = r[i]

        if VideoReturn:  # if it needs to return the frame with the detected tennis
            img_out = copy.copy(img)
            img_out = cv2.circle(img_out, (x_pos, y_pos), radius, (0,0,255), 1, 8, 0)
            return img_out, x_pos, y_pos, radius
        else:  # if it only needs to return the position of the detected tennis
            return x_pos, y_pos, radius





if __name__ == '__main__':
    try:
        detect = CarDetect()

        for i in range(33):

            img = cv2.imread('/home/mingrui/Mingrui/RaspberryCar/photo_tennis/tennis_'+ str(i) +'.jpg')

            img_out , x, y, r = detect.TennisDetect(img, VideoReturn=True)
            cv2.imshow('out'+str(i), img_out)
            cv2.waitKey(0)


    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        
