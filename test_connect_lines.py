import cv2
from sobel import sobel_xy
from util import substract_thresh, img_mark, substract_softthresh, abs_substract, get_sharp
import numpy as np

img = abs_substract
sharp = get_sharp(abs_substract)
gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
ret, gray_thresh = cv2.threshold(gray, thresh=60, maxval=255, type=cv2.THRESH_BINARY)
# 边缘检测
edges = cv2.Canny(img, 100, 200)

# 霍夫变换直线检测
lines = cv2.HoughLinesP(gray_thresh, 1, np.pi / 2, 30, minLineLength=10, maxLineGap=10)

# 绘制直线段
for line in lines:
    x1,y1,x2,y2 = line[0]

    # 计算直线的斜率
    k = (y2 - y1) / (x2 - x1 + 0.001)

    # 如果斜率在 -0.5~0.5 之间，则认为是竖直直线
    if abs(k) > 0.5:
        # 检测直角
        for l in lines:
            x3,y3,x4,y4 = l[0]
            if abs(y2-y3)<10 and abs(x1-x4)<10:
                cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.line(img,(x3,y3),(x4,y4),(0,255,0),2)
                cv2.circle(img, (x1, y1), 3, (0,0,255), -1)
                cv2.circle(img, (x2, y2), 3, (0,0,255), -1)
                cv2.circle(img, (x3, y3), 3, (0,0,255), -1)
                cv2.circle(img, (x4, y4), 3, (0,0,255), -1)





# 显示图像
cv2.imshow("abs_substract", abs_substract)
cv2.imshow("gray", gray)
cv2.imshow("gray_thresh", gray_thresh)
# cv2.imshow("edges", edges)
cv2.imshow("sharp", sharp)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(len(lines))

cv2.imwrite("abssubstract_gray_thresh.jpg", gray_thresh)