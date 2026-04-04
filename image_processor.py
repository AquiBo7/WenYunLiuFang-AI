import cv2
import numpy as np
from PIL import Image


def apply_ink_filter(img_path, output_path="ink_temp.jpg"):
    try:

        file_bytes = np.fromfile(img_path, dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None: return None


        # 灰度化
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 颜色反转
        inv_img = 255 - gray_img
        # 高斯模糊
        blur_img = cv2.GaussianBlur(inv_img, ksize=(21, 21), sigmaX=0, sigmaY=0)
        # 线性减淡融合
        blend_img = cv2.divide(gray_img, 255 - blur_img, scale=256)

        # 增强墨色对比度
        # 将淡灰色强制转为白色，加深墨色线条
        _, mask = cv2.threshold(blend_img, 220, 255, cv2.THRESH_BINARY)
        # 融合原灰度图，保留体积感
        final_img = cv2.multiply(blend_img, mask, scale=1 / 255)

        # 保存并转回PIL供Streamlit显示
        cv2.imwrite(output_path, final_img)
        return Image.open(output_path)
    except Exception as e:
        print(f"[ERROR] Ink Filter Failed: {e}")
        return None