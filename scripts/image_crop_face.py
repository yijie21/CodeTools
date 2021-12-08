# 人脸识别所需的文件：https://github.com/opencv/opencv/tree/4.x/data/haarcascades
import cv2
import os
import glob
import threading
#最后剪裁的图片大小
size_m = 64
size_n = 64
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects

cascade = cv2.CascadeClassifier("D:/Code/CodeTools/assets/haarcascade_frontalface_alt2.xml")
imglist = glob.glob("D:/datasets/debug/*")
cnt = 0
for list in imglist:
    img = cv2.imread(list)
    try:
        if img.shape[0] < 64 or img.shape[1] < 64:
            continue
    except:
        print(list)
    dst=img
    rects=detect(dst,cascade)
    for x1,y1,x2,y2 in rects:
        center = [(y1 + y2) // 2, (x1 + x2) // 2]
        y_left = center[0] - 32
        y_right = center[0] + 32
        x_left = center[1] - 32
        x_right = center[1] + 32
        if y_left < 0:
            y_right -= y_left
            y_left = 0
        if x_left < 0:
            x_right -= x_left
            x_left = 0
        roi = dst[y_left: y_right, x_left: x_right]
        f = "{}/{}".format("D:/datasets", "crop")
        if not os.path.exists(f):
            os.mkdir(f)
        cv2.imwrite("{}/{}.jpg".format(f, cnt), roi)
        cnt += 1
