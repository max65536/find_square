import cv2
import easyocr

# 加载图片
img = cv2.imread('nsmail-1.jpg')

# 定位到文本位置
text_detector = cv2.text.TextDetectorCNN_create('textbox.prototxt', 'TextBoxes_icdar13.caffemodel')
rects, scores = text_detector.detect(img)

# 对每个文本区域进行识别
reader = easyocr.Reader(['ch_sim', 'en'])
for rect in rects:
    x, y, w, h = rect.astype(int)
    # 裁剪文本区域，并进行OCR识别
    cropped_img = img[y:y+h, x:x+w]
    result = reader.readtext(cropped_img, detail=0)
    print(result)