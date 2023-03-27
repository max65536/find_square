import cv2
import numpy as np

# 加载两个图像并提取红色通道
img1 = cv2.imread('nsmail.jpg')
img2 = cv2.imread('nsmail-1.jpg')
red_channel1 = img1[:, :, 2]   # 提取红色通道
red_channel2 = img2[:, :, 2]

cv2.imwrite("images/img1_read.jpg", red_channel1)
cv2.imwrite("images/img2_read.jpg", red_channel2)
# 计算两个红色通道图像的差
diff = cv2.absdiff(red_channel1, red_channel2)
cv2.imwrite("images/diff.jpg", diff)
canny = cv2.Canny(diff, 50, 150)
cv2.imwrite("images/canny.jpg", canny)

kernel = np.ones((3,3), np.uint8)
dilated = cv2.dilate(canny, kernel, iterations=1)
cv2.imwrite("images/dilated.jpg", dilated)

lines = cv2.HoughLinesP(dilated, 1, np.pi / 180, 100, minLineLength=20, maxLineGap=10)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img1, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imwrite("images/lines.jpg", img1)
print(lines)