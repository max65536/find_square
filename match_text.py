import cv2
import numpy as np
from IPython import embed
from util import img_mark

# icon = cv2.imread('extract/icon.png', 0)
# image = cv2.imread('extract/grey_sharp.jpg', 0)
image_mark = cv2.imread('')
icon = cv2.imread('icons/rongqi.png', 0)
image = cv2.imread('input/grey_sharp.jpg', 0)

# image = abs_substract

cv2.imshow("icon", icon)

# 检查模板图像是否比原始图像大
if icon.shape[0] > image.shape[0] or icon.shape[1] > image.shape[1]:
    raise ValueError('Template image size must be smaller than source image size')

# 使用模板匹配功能进行匹配
result = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 设置匹配的阈值，这里设为0.8
threshold = 0.35

# 找到所有匹配的位置
locations = np.where(result >= threshold)


# for other_loc in zip(*locations[::-1]):
#     #第二次筛选----将位置偏移小于5个像素的结果舍去
#     if (temp_loc[0]+5<other_loc[0])or(temp_loc[1]+5<other_loc[1]):
#         numOfloc = numOfloc + 1
#         temp_loc = other_loc
#         cv2.rectangle(target,other_loc,(other_loc[0]+twidth,other_loc[1]+theight),(0,0,225),2)

strmin_val = str(min_val)
#初始化位置参数
temp_loc = min_loc
other_loc = min_loc
numOfloc = 1

# 在原始图像上用矩形标注所有匹配的位置
h = icon.shape[0]
w = icon.shape[1]
for other_loc in zip(*locations[::-1]):
    if (temp_loc[0]+5<other_loc[0])or(temp_loc[1]+5<other_loc[1]):
        numOfloc = numOfloc + 1
        temp_loc = other_loc
        cv2.rectangle(img_mark, other_loc, (other_loc[0] + w, other_loc[1] + h), (0, 0, 255), 1)

# 显示结果图像
cv2.imshow('Result', img_mark)
# cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(locations)
# print(result)
# embed()