import cv2
import numpy as np

# 读取图片
img = cv2.imread('nsmail-1.jpg')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 使用Otsu二值化处理
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 定义卷积核
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# 腐蚀图像
erode = cv2.erode(binary, kernel)

# 膨胀图像
dilate = cv2.dilate(erode, kernel)

# 连通组件分析
_, labels = cv2.connectedComponents(dilate)

# 获取每个连通组件的大小
sizes = cv2.countNonZero(labels, axis=1)

# 获取要去除的连通组件索引
remove_idx = np.argwhere(sizes < 100)

# 将要去除的连通组件设为背景色
for idx in remove_idx:
    labels[labels == idx] = 0

# 将其余连通组件设为前景色
labels[labels > 0] = 255

# 显示结果
cv2.imshow('result', labels)
cv2.waitKey(0)
cv2.destroyAllWindows()
