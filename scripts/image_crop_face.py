# 人脸识别所需的文件：https://github.com/opencv/opencv/tree/4.x/data/haarcascades
import cv2
import os
import glob
import threading
#最后剪裁的图片大小
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(90, 90), maxSize=(128, 128), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects

cascade = cv2.CascadeClassifier("D:/Code/CodeTools/assets/haarcascade_frontalface_default.xml")
imglist = glob.glob(os.path.join("D:/datasets/stars/", "*.jpg"))
cnt = 0
for list in imglist:
    img = cv2.imread(list)
    try:
        if img.shape[0] < 128 or img.shape[1] < 128:
            continue
        dst=img
        rects=detect(dst,cascade)
        for x1,y1,x2,y2 in rects:
            center = [(y1 + y2) // 2, (x1 + x2) // 2]
            y_left = center[0] - 64
            y_right = center[0] + 64
            x_left = center[1] - 64
            x_right = center[1] + 64
            if y_left < 0:
                y_right -= y_left
                y_left = 0
            if x_left < 0:
                x_right -= x_left
                x_left = 0
            roi = dst[y_left: y_right, x_left: x_right]
            f = "{}/{}".format("D:/datasets", "stars_crop")
            if not os.path.exists(f):
                os.mkdir(f)
            cv2.imwrite("{}/{:0>6}.jpg".format(f, cnt), roi)
            cnt += 1
    except:
        print(list)
        pass
    continue
    