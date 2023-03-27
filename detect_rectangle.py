import cv2
import numpy as np
from util import abs_substract, get_sharp

# 读取图片
img = abs_substract
sharp = get_sharp(abs_substract)
gray = cv2.cvtColor(sharp,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5,5), 0)

# 检测直线
edges = cv2.Canny(gray, 50, 150)

# 使用霍夫变换寻找直线
lines = cv2.HoughLinesP(edges,1,np.pi/2,100,minLineLength=50,maxLineGap=10)

# 遍历检测到的直线
for line in lines:
    x1,y1,x2,y2 = line[0]

    # 计算直线的斜率
    k = (y2 - y1) / (x2 - x1 + 0.001)

    # 判断水平直线和竖直直线
    if abs(k) > 50:
        # 竖直直线
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    elif abs(k) < 0.02:
        # 水平直线
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)

# 显示处理后的图片
cv2.imshow('image',img)
cv2.waitKey()
cv2.destroyAllWindows()