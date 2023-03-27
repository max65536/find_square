import cv2
import numpy as np

# 读取原始图像和标记图像
img1 = cv2.imread('nsmail.jpg')
img2 = cv2.imread('nsmail-1.jpg')

# 将图像转换为灰度图像
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 创建标记模板
template = cv2.imread('template.jpg', 0)

# 在无标记的图像中匹配标记模板
res = cv2.matchTemplate(gray1, template, cv2.TM_CCOEFF_NORMED)

# 获取匹配结果的最大值和最小值
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# 在有标记的图像中提取标记部分
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
marked_area = img2[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

# 显示提取出来的标记部分
cv2.imshow('Extracted Mark', marked_area)
cv2.waitKey(0)

# 保存提取出来的标记部分
cv2.imwrite('extracted_mark.jpg', marked_area)

# 关闭所有窗口
cv2.destroyAllWindows()