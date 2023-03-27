import cv2
import numpy as np
from IPython import embed
from util import substract, diff, img_orig, img_mark, diff_thresh, abs_substract
from util import get_hsv_mask, get_sharp

# 打开图片并进行颜色极端化处理
img = img_mark

sharp = get_sharp(abs_substract)

b, g, r = cv2.split(sharp)

# 取三个通道的均值
gray = cv2.addWeighted(b, 1/3, g, 1/3, 0)
gray = cv2.addWeighted(gray, 1, r, 1/3, 0)

abs_substract_hsv = cv2.cvtColor(abs_substract, cv2.COLOR_BGR2HSV)
sharp_hsv = cv2.cvtColor(sharp, cv2.COLOR_BGR2HSV)


# 显示处理后的灰度图片
cv2.imshow('abs_substract', abs_substract)
cv2.imshow('abs_substract_hsv', abs_substract_hsv)
cv2.imshow('sharp_hsv', sharp_hsv)
cv2.imshow('Processed Image', gray)
cv2.imshow('sharp', sharp)

cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存处理后的图片
# cv2.imwrite('example_processed.jpg', img_processed)
