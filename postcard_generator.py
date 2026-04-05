import io
from PIL import Image, ImageDraw, ImageFont
import streamlit as st


class PostcardGenerator:
    def __init__(self, font_name="Kaiti.ttf"):
        try:

            self.font = ImageFont.truetype(font_name, 24)
            self.title_font = ImageFont.truetype(font_name, 36, encoding="utf-8")
        except IOError:
            st.error(f"❌ 未在项目根目录找到字体文件 {font_name}，请务必上传，否则明信片将显示乱码。")
            self.font = ImageFont.load_default()
            self.title_font = ImageFont.load_default()

        self.text_color = (92, 58, 33)
        self.line_spacing = 10

    def wrap_text(self, text, draw, max_width):
        lines = []
        if draw.textbbox((0, 0), text, font=self.font)[2] <= max_width:
            lines.append(text)
        else:
            words = list(text)
            current_line = ""
            for word in words:
                test_line = current_line + word
                bbox = draw.textbbox((0, 0), test_line, font=self.font)
                if bbox[2] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
        return lines

    def generate(self, user_image_path, poem_title, poem_author, analysis_text, phase_tag):
        canvas_width = 1200
        canvas_height = 800
        postcard = Image.new('RGB', (canvas_width, canvas_height), color=(248, 244, 230))
        draw = ImageDraw.Draw(postcard)

        try:
            user_img = Image.open(user_image_path)
            user_img.thumbnail((550, 700))

            img_x = 30
            img_y = (canvas_height - user_img.height) // 2
            postcard.paste(user_img, (img_x, img_y))

            border_rect = [img_x - 5, img_y - 5, img_x + user_img.width + 5, img_y + user_img.height + 5]
            draw.rectangle(border_rect, outline=(139, 115, 85), width=2)

        except Exception as e:
            st.warning(f"明信片合成时读取图片失败: {e}")

        text_area_start_x = 620
        text_area_width = 550

        current_y = 80

        title_str = f"《{poem_title}》 - {poem_author}"
        draw.text((text_area_start_x, current_y), title_str, font=self.title_font, fill=self.text_color)
        current_y += 60

        draw.text((text_area_start_x, current_y), f"[{phase_tag}语文教材锚定]", font=self.font, fill=(139, 115, 85))
        current_y += 50

        short_analysis = analysis_text[:150] + "..." if len(analysis_text) > 150 else analysis_text

        lines = self.wrap_text(short_analysis, draw, text_area_width)
        for line in lines:
            draw.text((text_area_start_x, current_y), line, font=self.font, fill=self.text_color)
            current_y += draw.textbbox((0, 0), line, font=self.font)[3] + self.line_spacing

        img_byte_arr = io.BytesIO()
        postcard.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        return postcard, img_byte_arr