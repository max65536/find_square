import cv2
import numpy as np
from IPython import embed

# 加载图像
image = cv2.imread('nsmail-1.jpg')

# 转换颜色空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 定义红色范围
lower_red = np.array([0, 50, 50])
upper_red = np.array([20, 255, 255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)

lower_red = np.array([160, 50, 50])
upper_red = np.array([180, 255, 255])
mask2 = cv2.inRange(hsv, lower_red, upper_red)

# 合并两个遮罩
mask = mask1 + mask2

# 提取红色线条
red_lines = cv2.bitwise_and(image, image, mask=mask)

# embed()
# 显示提取结果
cv2.imwrite("cover_red.jpg", red_lines)
# cv2.imshow('Red lines', red_lines)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
