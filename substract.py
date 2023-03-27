import cv2

# 加载两个图像
img1 = cv2.imread('nsmail.jpg')
img2 = cv2.imread('nsmail-1.jpg')

height, width, channels = img1.shape
print('Image size: {} x {} pixels'.format(width, height))
# 计算两个图像的差
diff = cv2.subtract(img1, img2)

# 显示差异图像
cv2.imshow('Difference', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()
