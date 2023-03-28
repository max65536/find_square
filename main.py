import cv2
import numpy as np
from scan import scan, points_to_rectangles
from util import get_sharp
from IPython import embed
import math
from PIL import ImageFont, ImageDraw, Image

def get_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def get_abssub(img1, img2):
    return cv2.absdiff(img_mark, img_orig)

def detect_squares(abs_substract):
    sharp = get_sharp(abs_substract)
    gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
    ret, gray_thresh = cv2.threshold(gray, thresh=60, maxval=255, type=cv2.THRESH_BINARY)
    new_image, points = scan(gray_thresh)
    rects = points_to_rectangles(new_image, points)
    
    return rects

def get_extent(img_gray):
    pass

def match_text(icon, target, redundent=5):
    # 检查模板图像是否比原始图像大
    if icon.shape[0] > target.shape[0] or icon.shape[1] > target.shape[1]:
        raise ValueError('Template image size must be smaller than source image size')
    # 使用模板匹配功能进行匹配
    result = cv2.matchTemplate(target, icon, cv2.TM_CCOEFF_NORMED)
    cv2.imwrite("output/text_recog.jpg", result * 255)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 设置匹配的阈值，这里设为0.35
    threshold = 0.35
    # 找到所有匹配的位置
    locations = np.where(result >= threshold)    
    
    new_locations = []
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
            new_locations.append(other_loc)
            cv2.rectangle(img_mark, other_loc, (other_loc[0] + w, other_loc[1] + h), (0, 0, 255), 1)
    # embed()         
    # print("new_locations:", new_locations)   
    return new_locations

def get_text_pos(name, icon, target):
    # 返回的是左上角的坐标
    icon_gray = get_gray(icon)
    locations = match_text(icon=icon_gray, target=target)
    item_locs = {}
    for i, loc in enumerate(locations):
        item_locs["%s_%d"%(name, i+1)] = loc
    return item_locs

def get_distance(start, target):
    return math.sqrt((target[0]-start[0])**2 + (target[1]-start[1])**2)

def match_rect_text(rect_locs, item_locs, item_height):
    flags = [False] * len(rect_locs)
    pairs = {}
    for name, loc in item_locs.items():

        min_distance = 100000
        text_point = (loc[0]+item_height, loc[1])
        select = None
        select_point = None
        for i, (left_point, right) in enumerate(rect_locs):
            # print(i)
            if flags[i]:
                continue            
            distance = get_distance(text_point, left_point)
            if distance<min_distance:
                min_distance = distance
                select_point = [left_point, right]
                select = i

        # print(min_distance, select)
        # print(name, select_point)
        # print(flags)
        if select_point is not None:
            flags[select] = True
            pairs[name] = select_point
        
    return pairs


def draw_rects(imgname, rects):
    img = cv2.imread(imgname)
    for rect in rects:
        cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1) 
    cv2.imwrite("output/rects.jpg", img)   

def draw_text(img, item_pairs, text_height, text_width=None, text="test"):
    font = ImageFont.truetype("simsun.ttf", size=16, encoding="utf-8")
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    # draw.text((50, 80),  "端午节就要到了。。。", font = font, fill = (b, g, r, a))
    for name, rect in item_pairs.items():
        # cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1)
        # cv2.putText(img,  text, (rect[0][0], rect[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
        draw.text((rect[0][0], rect[0][1]-text_height), name, font = font, fill = (255,0,0))
    img = np.array(img_pil)
    for name, rect in item_pairs.items():
        cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1)    
    cv2.imwrite("output/generate.jpg", img)



# 读入文件
orig_path = "input/test.jpg"
mark_path = "input/test_mark.jpg"
img_orig = cv2.imread("input/test.jpg")
img_mark = cv2.imread("input/test_mark.jpg")

# 预处理
abs_substract = get_abssub(img_mark, img_orig)
sharp = get_sharp(abs_substract)
sharp_gray = get_gray(sharp)

# 找矩形框
rects = detect_squares(abs_substract)
# for rect in rects:
#         cv2.rectangle(img_orig, rect[0], rect[1], (0,0,255), 1)

# 找文字        
icon = cv2.imread("icons/rongqi.png")
locations = get_text_pos(name="容器", icon=icon, target=sharp_gray)
print(locations)

# 匹配文字和框
item_pairs = match_rect_text(rect_locs=rects, item_locs=locations, item_height=40)

cv2.imshow("sharp", sharp)
cv2.imshow("sharp_gray", sharp_gray)
cv2.imshow("img_mark", img_mark)

cv2.waitKey(0)
# # embed()
cv2.destroyAllWindows()

# 输出到output
cv2.imwrite("output/sharp.jpg", sharp)
cv2.imwrite("output/sharp_gray.jpg", sharp_gray)
print("rect locations:", rects)
print("text locations:", locations)
print(item_pairs)
draw_text(img_orig, item_pairs=item_pairs, text_height=16)
draw_rects(orig_path, rects)


# embed()




