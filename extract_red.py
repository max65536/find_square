import cv2
import numpy as np

# 读取原始图片和带有红色标记的图片
image = cv2.imread('nsmail.jpg')
overlay = cv2.imread('nsmail-1.jpg')

# 提取红色通道
red_channel = overlay[:,:,2]
cv2.imwrite("extract/red_channel.jpg", red_channel)

# 创建alpha通道
alpha_channel = np.zeros(red_channel.shape, dtype=red_channel.dtype)
alpha_channel[red_channel > 0] = 255
cv2.imwrite("extract/alpha_channel.jpg", alpha_channel)
# 合并图像和alpha通道
output = cv2.merge((overlay[:,:,0], overlay[:,:,1], alpha_channel))
cv2.imwrite("extract/output.jpg", output)

# 将红色标记应用于原始图片
overlay_mask = output[:, :, 2]
cv2.imwrite("extract/overlay_mask1.jpg", overlay_mask)
overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
cv2.imwrite("extract/overlay_mask2.jpg", overlay_mask)
output = cv2.addWeighted(image, 1, output, 0.5, 0)

# 显示结果
cv2.imshow("Red Overlay", output)
cv2.waitKey(0)
cv2.destroyAllWindows()