import cv2
import numpy as np
from scan import scan, points_to_rectangles
from util import get_sharp
from IPython import embed
import math
from PIL import ImageFont, ImageDraw, Image
from gen_cn import gen_all_labels
import logging

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def get_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def get_abssub(img1, img2):
    return cv2.absdiff(img1, img2)

def detect_squares(abs_substract):
    sharp = get_sharp(abs_substract)
    gray = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
    ret, gray_thresh = cv2.threshold(gray, thresh=60, maxval=255, type=cv2.THRESH_BINARY)
    cv2.imwrite("tmp/sharp_gray_thresh.jpg", gray_thresh)
    new_image, points = scan(gray_thresh)
    rects = points_to_rectangles(new_image, points)
    cv2.imwrite("tmp/vertex.jpg", new_image)
    return rects

def get_extent(img_gray):
    pass

def match_text(icon, target, threshold, redundent=5):
    # 检查模板图像是否比原始图像大
    if icon.shape[0] > target.shape[0] or icon.shape[1] > target.shape[1]:
        raise ValueError('Template image size must be smaller than source image size')
    # 使用模板匹配功能进行匹配
    result = cv2.matchTemplate(target, icon, cv2.TM_CCOEFF_NORMED)
    cv2.imwrite("tmp/text_recog.jpg", result * 255)
    logging.info("max recog:"+str(result.max()))
    # cv2.imshow("text_result", result)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 设置匹配的阈值，这里设为0.35
    threshold = threshold
    # 找到所有匹配的位置
    locations = np.where(result >= threshold)    
    logging.info("raw text locations" + str(locations))
    new_locations = []
    temp_loc = [0, 0]
    other_loc = [0, 0]
    numOfloc = 1
    # 在原始图像上用矩形标注所有匹配的位置
    h = icon.shape[0]
    w = icon.shape[1]
    logging.info("max_val: " +  str(max_val))
    logging.info("threshold: " +  str(threshold))
    for other_loc in zip(*locations[::-1]):
        # logging.info(str(temp_loc)+'  '+str(other_loc))
        # if result[other_loc[0]][other_loc[1]]<threshold:
        #     continue
        if (temp_loc[0]+5<other_loc[0])or(temp_loc[1]+5<other_loc[1]):
            numOfloc = numOfloc + 1
            temp_loc = other_loc
            new_locations.append(other_loc)
            cv2.rectangle(img_mark, other_loc, (other_loc[0] + w, other_loc[1] + h), (255, 0, 0), 1)
    # embed()         
    # print("new_locations:", new_locations)   
    cv2.imwrite("tmp/all_texts.jpg", img_mark)
    logging.info("new text locations" + str(new_locations))
    return new_locations, result

def get_text_pos(name, icon, target, threshold):
    # 返回的是左上角的坐标
    icon_gray = get_gray(icon)
    cv2.imwrite("tmp/gray_icon.png",icon_gray)
    locations, result = match_text(icon=icon_gray, target=target, threshold=threshold)
    item_locs = {}
    scores = {}
    for i, loc in enumerate(locations):
        item_locs["%s_%d"%(name, i+1)] = loc
        scores["%s_%d"%(name, i+1)] = result[loc[1]][loc[0]]
    # embed()
    return item_locs, scores

def get_distance(start, target):
    return math.sqrt((target[0]-start[0])**2 + (target[1]-start[1])**2)

def match_rect_text(rect_locs, item_locs, item_height, scores):
    flags = [False] * len(rect_locs)
    min_distance = 10
    pairs = {}

    for i, (left_point, right) in enumerate(rect_locs):
        max_score = 0
        select = None
        select_point = None
        for name, loc in item_locs.items():
            if flags[i]:
                continue        
            text_point = (loc[0], loc[1]+item_height)    
            distance = get_distance(text_point, left_point)
            if distance<min_distance and scores[name]>max_score:
                print(distance)
                max_score = scores[name]
                select_point = [left_point, right]
                select = name                
            # if distance<30 and score
        # print(name, select_point)
        # print(flags)
        if select_point is not None:
            pairs[select] = select_point
        
    return pairs


def draw_rects(imgname, rects):
    img = cv2.imread(imgname)
    for rect in rects:
        cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1) 
    cv2.imwrite("output/rects.jpg", img)   

def draw_texts(imgname, item_locs):
    pass
    # img = cv2.imread(imgname)
    # for loc in item_locs:
    #     cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1) 
    # cv2.imwrite("output/rects.jpg", img)       

def draw_text_rects(img, item_pairs, text_height, text_width=None, text="test"):
    font = ImageFont.truetype("simsun.ttf", size=16, encoding="utf-8")
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    for name, rect in item_pairs.items():
        # cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1)
        # cv2.putText(img,  text, (rect[0][0], rect[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
        draw.text((rect[0][0], rect[0][1]-text_height), name, font = font, fill = (255,0,0))
    img = np.array(img_pil)
    for name, rect in item_pairs.items():
        cv2.rectangle(img, rect[0], rect[1], (255,0,0), 1)    
    cv2.imwrite("output/generate.jpg", img)



# 读入文件
# orig_path = "input/复杂/2/_20220901084715808.jpg"
# mark_path = "input/复杂/2/_202209201084715808.jpg"
orig_path = "input/test.jpg"
mark_path = "input/test_mark.jpg"
img_orig = cv2.imread(orig_path)
img_mark = cv2.imread(mark_path)

# 预处理
abs_substract = get_abssub(img_mark, img_orig)
sharp = get_sharp(abs_substract)
sharp_gray = get_gray(sharp)

# 找矩形框
rects = detect_squares(abs_substract)
# for rect in rects:
#         cv2.rectangle(img_orig, rect[0], rect[1], (0,0,255), 1)

# 生成labels
labels = ["电子设备","电池", "管制器具", "容器", "雨伞","压力容器","火种","食品"]
gen_all_labels(labels=labels, size=17, fill=(255,255,255,255))

# 找文字        
# label = "雨伞"
# icon = cv2.imread("icons/%s.png"%label)
# locations, scores  = get_text_pos(name=label, icon=icon, target=sharp_gray, threshold=0.35)
# print("locations:", locations)
# print("scores",scores)


all_scores = {}
all_locations = {}
for label in labels:
    icon = cv2.imread("icons/%s.png"%label)
    locations, scores = get_text_pos(name=label, icon=icon, target=sharp_gray, threshold=0.35)  
    # for label, loc in locations.items():        
    all_scores.update(scores)
    all_locations.update(locations)

label = "容器"
icon = cv2.imread("icons/%s.png"%label)
locations, scores = get_text_pos(name=label, icon=icon, target=sharp_gray, threshold=0.35)
print("locations:",all_locations)
print("scores:",all_scores)


# 匹配文字和框
item_pairs = match_rect_text(rect_locs=rects, item_locs=all_locations, item_height=17, scores=all_scores)

# cv2.imshow("sharp", sharp)
# cv2.imshow("sharp_gray", sharp_gray)
# cv2.imshow("img_mark", img_mark)

# cv2.waitKey(0);cv2.destroyAllWindows()

# 输出到output
cv2.imwrite("output/sharp.jpg", sharp)
cv2.imwrite("output/sharp_gray.jpg", sharp_gray)
print("rect locations:", rects)
print("text locations:", locations)
print(item_pairs)

draw_text_rects(img_orig, item_pairs=item_pairs, text_height=16)
draw_rects(orig_path, rects)
draw_texts(orig_path, item_locs=locations)


# embed()




