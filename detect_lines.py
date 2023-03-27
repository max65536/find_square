import cv2
from IPython import embed
import numpy as np

# 加载两个图像并提取红色通道
img1 = cv2.imread('nsmail.jpg')
img2 = cv2.imread('nsmail-1.jpg')
red_channel1 = img1[:, :, 2]   # 提取红色通道
red_channel2 = img2[:, :, 2]

# 计算两个红色通道图像的差
diff = cv2.absdiff(red_channel1, red_channel2)
blur = cv2.fastNlMeansDenoising(diff)
ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

# This returns an array of r and theta values
lines = cv2.HoughLines(thresh, 1, np.pi/180, 20)
print(lines)

# embed()
# The below for loop runs till r and theta values
# are in the range of the 2d array
for r_theta in lines:
    arr = np.array(r_theta[0], dtype=np.float64)
    r, theta = arr
    # Stores the value of cos(theta) in a
    a = np.cos(theta)
    # Stores the value of sin(theta) in b
    b = np.sin(theta)
    # x0 stores the value rcos(theta)
    x0 = a*r
    # y0 stores the value rsin(theta)
    y0 = b*r
    # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
    x1 = int(x0 + 1000*(-b))
    # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
    y1 = int(y0 + 1000*(a))
    # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
    x2 = int(x0 - 1000*(-b))
    # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
    y2 = int(y0 - 1000*(a))
  
    # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
    # (0,0,255) denotes the colour of the line to be
    # drawn. In this case, it is red.
    cv2.line(img1, (x1, y1), (x2, y2), (0, 0, 255), 2)
  
# All the changes made in the input image are finally
# written on a new image houghlines.jpg

cv2.imwrite("detect_lines.jpg", img1)

# 显示差异图像
cv2.imwrite("red_channel.jpg", diff)
cv2.imwrite("denoise.jpg", blur)
cv2.imwrite("bin_red_channel.jpg", thresh)
