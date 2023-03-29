import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import os

## Make canvas and set the color
def gen_text_png(text, size, fill, out_dir="icons"):
    img = np.zeros((size, size*len(text),3),np.uint8)
    b,g,r,a = fill

    ## Use simsum.ttc to write Chinese.
    fontpath = r"fangzhengjunhei.ttf" # <== 这里是宋体路径 
    # fontpath = r"fangzhengpixel16.ttf" # <== 这里是宋体路径 
    # embed()
    font = ImageFont.truetype(fontpath, size=size, encoding="utf-8")
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((0, 0),  text, font = font, fill = fill)
    img = np.array(img_pil)

    ## Display 
    # cv2.imshow("res", img);cv2.waitKey();cv2.destroyAllWindows()
    cv2.imwrite(os.path.join(out_dir, "%s.png"%text), img)

def gen_all_labels(labels, size=30, out_dir="icons", fill=(0,0,255,0)):
    for label in labels:
        gen_text_png(label, size=size, out_dir=out_dir, fill=fill)
