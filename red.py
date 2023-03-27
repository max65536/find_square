import cv2
from IPython import embed
import numpy as np

# 加载两个图像并提取红色通道
img1 = cv2.imread('nsmail.jpg')
img2 = cv2.imread('nsmail-1.jpg')
red_channel1 = img1[:, :, 2]   # 提取红色通道
red_channel2 = img2[:, :, 2]

# 计算两个红色通道图像的差
diff = cv2.absdiff(red_channel1, red_channel2)
blur = cv2.fastNlMeansDenoising(diff)
ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# 显示差异图像
cv2.imwrite("red_channel.jpg", diff)
cv2.imwrite("denoise.jpg", blur)
cv2.imwrite("bin_red_channel.jpg", thresh)


def is_rectangle(mat, x, y, extend=10):
    if mat[x][y]==0:
        return False
    max_x, max_y = mat.shape
    x_count = 1
    count = 0
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
        

def scan(mat):
    new_mat = np.zeros(mat.shape)
    m,n = mat.shape
    for i in range(m):
        for j in range(n):
            if is_rectangle(mat, i, j, extend=20):
                print("angle: ", i, j)
                new_mat[i][j]=255
    return new_mat


dilated = cv2.imread("images/dilated.jpg", -1)
# print(dilated)
new_image = scan(dilated)
cv2.imwrite("new_image_dilated.jpg", new_image)


# print(thresh.shape)
# embed()

# 轮廓检测
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # 绘制矩形轮廓并获取矩形顶点坐标
# for contour in contours:
#     # 计算轮廓的面积和周长
#     area = cv2.contourArea(contour)
#     perimeter = cv2.arcLength(contour, True)
#     # 判断是否为矩形
#     if area > 100 and perimeter < 2000:
#         x, y, w, h = cv2.boundingRect(contour)
#         # 计算矩形的四个顶点坐标
#         pt1 = (x, y)
#         pt2 = (x + w, y)
#         pt3 = (x + w, y + h)
#         pt4 = (x, y + h)
#         # 绘制矩形轮廓
#         cv2.rectangle(img1, pt1, pt3, (0, 0, 255), 2)
#         # 输出矩形的四个顶点坐标
#         # print('矩形顶点坐标：')
#         # print(pt1)
#         # print(pt2)
#         # print(pt3)
#         # print(pt4)


# cv2.imwrite("regenerate.jpg", img1)
