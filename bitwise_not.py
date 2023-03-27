import cv2
path = 'images/dilated.jpg'
img = cv2.imread(path)
img_revert = cv2.bitwise_not(img)
# print(img_revert)
cv2.imwrite(path.split('.')[0]+'_not.jpg', img_revert)