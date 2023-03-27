import cv2
import numpy as np
# img = cv2.imread('nsmail-1.jpg')
# img = cv2.imread('images/canny.jpg')
img = cv2.imread('bin_red_channel.jpg')
img = cv2.bitwise_not(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)

rects = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area < 100:
        continue
    rect = cv2.minAreaRect(contour)
    (x, y), (w, h), angle = rect
    if h > w:
        w, h = h, w
        angle += 90
    if w / h > 1.5:
        continue
    rects.append(rect)

for rect in rects:
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()