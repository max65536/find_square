from PIL import Image

# 打开图片并进行颜色极端化处理
img = Image.open("nsmail-1.jpg")
img = Image.eval(img, lambda x: x * 3) # 增强颜色饱和度
img = Image.eval(img, lambda x: x + 5) # 调整亮度
img.show() # 启动图片查看器展示图片
img.save("enchant_color.jpg") # 保存图片到本地