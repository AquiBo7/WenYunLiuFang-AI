from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io


class ReportEngine:
    def __init__(self, font_path="NotoSerifSC-Regular.otf"):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            self.font_name = 'CustomFont'
        except:
            self.font_name = 'Helvetica'  # 兜底

    def generate_pdf(self, user_data):

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        c.setFont(self.font_name, 22)
        c.drawCentredString(width / 2, height - 50, "【文韵流芳】AI 研学报告")
        c.setLineWidth(1)
        c.line(50, height - 65, width - 50, height - 65)

        c.setFont(self.font_name, 16)
        c.drawString(70, height - 100, f"主题作品：《{user_data['title']}》")
        c.setFont(self.font_name, 12)

        y_cursor = height - 130
        for line in user_data['content'].split('\n'):
            c.drawString(70, y_cursor, line)
            y_cursor -= 20

        y_cursor -= 30
        c.setFont(self.font_name, 14)
        c.drawString(70, y_cursor, "🏛️ 名家会诊意见：")
        y_cursor -= 25
        c.setFont(self.font_name, 10)

        for expert, text in user_data['critiques'].items():
            c.setFont(self.font_name, 11)
            c.drawString(70, y_cursor, f"【{expert}】：")
            y_cursor -= 18
            c.setFont(self.font_name, 10)

            text_lines = [text[i:i + 45] for i in range(0, len(text), 45)]
            for t_line in text_lines:
                c.drawString(90, y_cursor, t_line)
                y_cursor -= 15
            y_cursor -= 10

        c.setFont(self.font_name, 8)
        c.drawCentredString(width / 2, 30, "技术支持：文脉智绘引擎 | 仅供学术交流使用")

        c.showPage()
        c.save()
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes