import cv2
import numpy as np

# 读取原始图片和标记图片
image = cv2.imread('nsmail.jpg')
mask = cv2.imread('nsmail-1.jpg')

# 将原始图片和标记图片转换为HSV色彩空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hsv_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 50, 50])
upper_red = np.array([20, 255, 255])
mask1 = cv2.inRange(hsv_mask, lower_red, upper_red)

lower_red = np.array([160, 50, 50])
upper_red = np.array([180, 255, 255])
mask2 = cv2.inRange(hsv_mask, lower_red, upper_red)
red_mask = mask1 + mask2

# 将红色掩码应用于原始图像
output = cv2.bitwise_and(image, image, mask = red_mask)

# 显示结果
cv2.imshow("Red Region", output)
cv2.waitKey(0)
cv2.destroyAllWindows()