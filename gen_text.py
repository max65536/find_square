import cv2
import numpy as np
from util import img_orig

# arr = np.zeros((100,100,3))
# # cv2.addText(img_orig, "aaa", org=(10,10), nameFont="Times")
# cv2.putText(img_orig, text="HELLO", org=(100, 80), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,255), thickness=2)

# # cv2.imshow("text",img_orig) 
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
# blur = cv2.GaussianBlur(img_orig, (5,5), 0)
# cv2.imwrite("extract/img_hello.jpg", blur)

# 生成文字
# 定义窗口大小
height, width  = 80, 160
# 创建黑色背景的图像
image = 255 * np.ones((height, width, 3), np.uint8)
# 设置文本
text = "Hello"
# 设置字体
font = cv2.FONT_HERSHEY_SIMPLEX
# 设置字体大小
font_size = 2
# 设置字体颜色
font_color = (0, 0, 255)
# 设置文本放置的位置
position = (10, 50)

# 在黑色背景上写上文本并显示在OpenCV窗口中
cv2.putText(image, text, position, font, font_size, font_color, thickness=2)
cv2.imshow("Image with text", image)
cv2.waitKey(0)

cv2.imwrite("extract/text_image.png", image)

