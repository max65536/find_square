import numpy as np
import cv2
from IPython import embed
from util import abs_substract, get_sharp, img_mark, img_orig

def is_rectangle(mat, x, y, extend=10):
    if mat[x][y]==0:
        return False
    max_x, max_y = mat.shape
    x_count = 1
    # count = 0
    for i in range(x, x-extend, -1):
        if i<0 or mat[i][y]==0:
            x_count -= 1
            break
    x_count += 1
    for i in range(x, x+extend):
        if i>=max_x or mat[i][y]==0:
            x_count -= 1
            break        
    y_count = 1
    for j in range(y, y-extend, -1):
        if j<0 or mat[x][j]==0:
            y_count -= 1
            break 
    y_count += 1       
    for j in range(y, y+extend):
        if j>=max_y or mat[x][j]==0:
            y_count -= 1
            break                
    if x_count==1 and y_count==1:
        return True
    else:
        return False

def is_rectangle_skip(mat, x, y, extend=10):
    if mat[x][y]==0:
        return False
    max_x, max_y = mat.shape
    
    
    x_left = 0
    for i in range(x, x-extend, -1):
        if i<0 or mat[i][y]==0:
            continue
        x_left += 1

    x_right = 0
    for i in range(x, x+extend):
        if i>=max_x or mat[i][y]==0:
            continue
        x_right += 1     
    
    y_left = 0
    for j in range(y, y-extend, -1):
        if j<0 or mat[x][j]==0:
            continue
        y_left += 1

    y_right = 0   
    for j in range(y, y+extend):
        if j>=max_y or mat[x][j]==0:
            continue
        y_right += 1  

    threshold = extend//2
    if ((x_left>=threshold + x_right>=threshold)==1) and ((y_left>=threshold + y_right>=threshold)==1):
        return True
    else:
        return False    

def scan(mat):
    points = []
    new_mat = np.zeros(mat.shape)
    m = mat.shape[0]
    n = mat.shape[1]
    for i in range(m):
        for j in range(n):
            if is_rectangle(mat, i, j, extend=15):
                # print("angle: ", i, j)
                points.append((i, j))
                new_mat[i][j]=255
    return new_mat, points

def points_to_rectangles(image, points):
    ans = []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            pix, piy = points[i]
            pjx, pjy = points[j]
            if pjx-pix>5 and pjy-piy>5 and image[pix, pjy] and image[pjx, piy]:
                # 这里给反回来，不知道为什么反正可以
                image[pix, pjy]=0
                image[pjx, piy]=0
                ans.append([(piy, pix), (pjy, pjx)])
    
    return ans

img = abs_substract
sharp = get_sharp(abs_substract)
gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
ret, gray_thresh = cv2.threshold(gray, thresh=60, maxval=255, type=cv2.THRESH_BINARY)

new_image, points = scan(gray_thresh)

rects = points_to_rectangles(new_image, points)
for rect in rects:
    cv2.rectangle(img_orig, rect[0], rect[1], (0,0,255), 1)

# 将二值图像转换为3通道的彩色图像
binary_img = np.zeros_like(img_orig)  # 创建与彩色图像相同大小的空白图像
binary_img[new_image > 0] = (255, 255, 255)  # 将二值图像中白色部分的像素值设置为(255, 255, 255)，即转换为彩色图像
points_on_image = cv2.bitwise_or(abs_substract, binary_img)

# embed()

cv2.imshow("points_on_image", points_on_image)
cv2.imshow("gray_sharp_thresh", gray_thresh)
cv2.imshow("abs_substract", abs_substract)
cv2.imshow("new_image", new_image)
cv2.imshow("rects", img_orig)
cv2.imshow("mark", img_mark)
print(points)
print("rect:")
print(rects)

# embed()

cv2.waitKey(0)
# embed()
cv2.destroyAllWindows()
