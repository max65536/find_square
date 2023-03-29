import cv2
import numpy as np

def get_diff(img2, img1):
    # 加载两个图像并提取红色通道
    red_channel1 = img1[:, :, 2]   # 提取红色通道
    red_channel2 = img2[:, :, 2]
    # 计算两个红色通道图像的差
    diff = cv2.absdiff(red_channel2, red_channel1)
    return diff

def get_hsv_mask(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    s_min, v_min = [100, 100]
    s_max, v_max = [255, 255]
    lower_red = np.array([0, s_min, v_min])
    upper_red = np.array([20, s_max, v_max])
    mask1 = cv2.inRange(hsv_image, lower_red, upper_red)

    lower_red = np.array([160, s_min, v_min])
    upper_red = np.array([180, s_max, v_max])
    mask2 = cv2.inRange(hsv_image, lower_red, upper_red)
    red_mask = mask1 + mask2
    return red_mask

# 加载两个图像
# img_orig  = cv2.imread('nsmail.jpg')
# img_mark = cv2.imread('nsmail-1.jpg')
# img_mark_hsv = cv2.cvtColor(img_mark, cv2.COLOR_BGR2HSV)
# img_orig_hsv = cv2.cvtColor(img_orig, cv2.COLOR_BGR2HSV)

# height, width, channels = img_mark.shape
# print('Image size: {} x {} pixels'.format(width, height))
# # 计算两个图像的差

# abs_substract = cv2.absdiff(img_mark, img_orig)
# substract = cv2.subtract(img_mark, img_orig)
# hsv_substract = cv2.subtract(img_mark_hsv, img_orig_hsv)
# diff = get_diff(img_mark, img_orig)
# img_mark_hsv_red = get_hsv_mask(img_mark)

# # threshold
# thresh, diff_thresh = cv2.threshold(diff, thresh=39, maxval=255, type=cv2.THRESH_BINARY)
# thresh, substract_thresh = cv2.threshold(substract, thresh=36, maxval=255, type=cv2.THRESH_BINARY)
# thresh, substract_softthresh = cv2.threshold(substract, thresh=20, maxval=255, type=cv2.THRESH_TOZERO)

# substract_hsv = cv2.cvtColor(substract, cv2.COLOR_BGR2HSV)
# substract_hsv_red = get_hsv_mask(substract)
# substract_thresh_hsv_red = get_hsv_mask(substract_thresh)

def get_sharp(img):
    kernel = np.array([[-1,-1,-1],
                   [-1, 9,-1],
                   [-1,-1,-1]])
    sharp = cv2.filter2D(img,-1,kernel)
    return sharp

# B,G,R = cv2.split(substract)
# H,S,V = cv2.split(substract)

# cv2.imshow('B', B)
# cv2.imshow('G', G)
# cv2.imshow('R', R)

# cv2.imshow('H', H)
# cv2.imshow('S', S)
# cv2.imshow('V', V)

# cv2.imshow("hsv substract", hsv_substract)

# # 显示差异图像
# cv2.imshow('diff', diff)
# cv2.imshow('diff_thresh', diff_thresh)

# cv2.imshow('substract_soft', substract_softthresh)
# cv2.imshow('substract', substract_thresh)

# cv2.imshow('sharp', sharp)

# cv2.imshow('substract_thresh', substract_thresh)
# cv2.imshow('substract hsv', substract_hsv)
# cv2.imshow('substract hsv red', substract_hsv_red)

# cv2.imshow('substract thresh red', substract_thresh_hsv_red)

# cv2.imshow('image_mark', img_mark)
# cv2.imshow('image_hsv', img_mark_hsv)
# cv2.imshow('image_hsv_red', img_mark_hsv_red)


# cv2.imshow("mark",img_mark)
# cv2.imshow("orig",img_orig) 
# cv2.waitKey(0)
# cv2.destroyAllWindows()
