import cv2
import numpy as np

img = cv2.imread('nsmail-1.jpg')
img0 = cv2.imread('nsmail.jpg')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# lower_red = np.array([0, 50, 50])
# upper_red = np.array([10, 255, 255])
# mask = cv2.inRange(img_hsv, lower_red, upper_red)
# cv2.imwrite("images/mask1.jpg", mask)

lower_red = np.array([0, 50, 50])
upper_red = np.array([20, 255, 255])
mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

lower_red = np.array([160, 50, 50])
upper_red = np.array([180, 255, 255])
mask2 = cv2.inRange(img_hsv, lower_red, upper_red)
mask = mask1 + mask2
cv2.imwrite("images/mask1.jpg", mask)

# img1 = cv2.imread('nsmail.jpg')
# img2 = cv2.imread('nsmail-1.jpg')
# red_channel1 = img1[:, :, 2]   # 提取红色通道
# red_channel2 = img2[:, :, 2]

# diff = cv2.absdiff(red_channel1, red_channel2)
# cv2.imwrite("images/diff.jpg", diff)

kernel = np.ones((5,5),np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
cv2.imwrite("images/mask2.jpg", mask)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
cv2.imwrite("images/mask3.jpg", mask)

contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    area = cv2.contourArea(c)
    if area > 0:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img0, (x,y), (x+w,y+h), (0,255,0), 2)

cv2.imshow('result', img0)
cv2.waitKey(0)
cv2.destroyAllWindows()