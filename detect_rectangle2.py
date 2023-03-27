import cv2
import numpy as np
from util import abs_substract, img_mark

# img = cv2.imread('image.jpg')
img = abs_substract
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 通过阈值分割获取二值图像
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# 对二值图像进行形态学处理，去除噪声和填补孔洞
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) # 定义形态学结构元素
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) # 闭运算填补孔洞
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel) # 开运算去除噪点

# 查找所有轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历所有轮廓，过滤掉小的轮廓，仅保留大的轮廓
rectangles = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 10:
        continue
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) != 4:
        continue
    rectangles.append(approx)

# 针对每个矩形，计算其长宽比，以排除不是矩形的轮廓
count = 0
for rect in rectangles:
    x, y, w, h = cv2.boundingRect(rect)
    aspect_ratio = w / float(h)
    if aspect_ratio < 0.8 or aspect_ratio > 1.2:
        continue
    count += 1
    cv2.drawContours(img, [rect], 0, (0, 0, 255), 2)
    for p in rect:
        cv2.circle(img, tuple(p[0]), 5, (0, 255, 0), -1)


# 显示图像
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 打印检测到的矩形数量
print("Detected {} rectangles.".format(count))
print(contours)