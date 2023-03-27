import numpy as np
import cv2

# 定义HSV颜色的范围
hsv_min = np.array([0, 150, 100])
hsv_max = np.array([20, 255, 255])

# 创建一个空的十六进制颜色列表
colors = []

# 遍历指定HSV范围的每个像素
for h in range(hsv_min[0], hsv_max[0] + 1):
    for s in range(hsv_min[1], hsv_max[1] + 1):
        for v in range(hsv_min[2], hsv_max[2] + 1):
            # 将HSV值转换为BGR值
            bgr = cv2.cvtColor(np.array([[[h, s, v]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)[0][0]
            # 将BGR值转换为十六进制颜色
            hex_color = "#{:02x}{:02x}{:02x}".format(int(bgr[2]), int(bgr[1]), int(bgr[0]))
            colors.append(hex_color)

print(len(colors))

# 创建一个显示颜色的窗口
window_name = "HSV Colors"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 800, 600)

# 计算每个像素所需要的面积
num_colors = len(colors)
pixels_per_color = int(800 * 600 / num_colors)

# 创建一个800x600的白色图像
img = np.full((600, 800, 3), 255, dtype=np.uint8)

# 在图像上重复每种颜色
for i, color in enumerate(colors):
    y = int(i / (800 / pixels_per_color))
    x = int(i % (800 / pixels_per_color)) * pixels_per_color
    img[y:y + pixels_per_color, x:x + pixels_per_color] = cv2.cvtColor(np.array([[color]], dtype=np.uint8), cv2.COLOR_RGB2BGR)

# 显示图像并等待用户按下任意键
cv2.imshow(window_name, img)
cv2.waitKey(0)

# 销毁窗口
cv2.destroyAllWindows()