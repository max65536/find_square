import cv2
import numpy as np
 
# 读取图像并将其转换为灰度图像
img = cv2.imread('nsmail-1.jpg')

# 将图像转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用常量标量值指定灰度图像的阈值上下界
red_lower = (0, 0, 100)
red_upper = (0, 0, 255)

# 对灰度图像进行阈值处理，并只保留红色区域
red = cv2.inRange(gray, red_lower, red_upper)
 
# 对二进制图像进行轮廓检测
contours, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
# 标注红色方框
for c in contours:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    
# 显示标注后的图像
cv2.imshow('image', img)
cv2.waitKey(0)