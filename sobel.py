import cv2
import numpy as np
from util import substract, diff, img_orig, img_mark, diff_thresh
from util import get_hsv_mask


# 对灰度图像进行 Sobel 算子处理
sobel_y = cv2.Sobel(diff_thresh, cv2.CV_64F, 0, 1, ksize=3)
sobel_x = cv2.Sobel(diff_thresh, cv2.CV_64F, 1, 0, ksize=3)

sobel_xy = cv2.bitwise_or(sobel_x, sobel_y)
# 使用阈值将边缘提取出来
# ret, threshold = cv2.threshold(np.abs(sobel_y), 30, 255, cv2.THRESH_BINARY)

# sub_hsv = get_hsv_mask(substract)

# 显示处理后的图像
# cv2.imshow('Original Image', img2)
# cv2.imshow('Diff Image', diff)
# cv2.imshow('Substract Image', substract)
# cv2.imshow('Sub_hsv Image', sub_hsv)
# # cv2.imshow('Thresholded Image', threshold)
# cv2.imshow('sobel y', sobel_y)
# cv2.imshow('sobel x', sobel_x)
# cv2.imshow('or',cv2.bitwise_or(sobel_x,sobel_y))
# cv2.waitKey(0)
# cv2.destroyAllWindows()