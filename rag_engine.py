import json

class RAGEngine:
    def __init__(self, db_path="poems_db.json"):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
        except Exception as e:
            print(f"数据库加载失败: {e}")
            self.db = []

    def retrieve_poem(self, image_tags, target_phase):
        best_match = None
        max_overlap = 0

        for poem in self.db:
            if poem['phase'] != target_phase:
                continue

            overlap = len(set(image_tags) & set(poem['tags']))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = poem

        return best_match

    def build_prompt(self, image_tags, target_phase, matched_poem):
        system_roles = {
            "小学": "你是一位亲切的小学语文老师。用词必须极其简单、生动，多用比喻，鼓励为主。",
            "初中": "你是一位初中语文老师。重点分析诗句中的意境、修辞手法（如借景抒情、白描）。",
            "高中": "你是一位资深的高中语文名师。请结合知人论世的方法，深度剖析诗人的时代背景与复杂情感升华。"
        }

        role_setting = system_roles.get(target_phase, system_roles["小学"])
        tags_str = "、".join(image_tags)

        if matched_poem:
            prompt = f"""
            {role_setting}
            学生上传了一张图片，AI 视觉识别到的元素有：{tags_str}。
            请根据我们的教学大纲，为学生讲解以下这首诗：
            《{matched_poem['title']}》 - {matched_poem['author']}
            原文：{matched_poem['content']}
            必须覆盖的核心考点：{matched_poem['exam_point']}

            请直接给出讲解，排版要精美清晰。
            """
        else:
            prompt = f"""
            {role_setting}
            学生上传了一张图片，AI 视觉识别到的元素有：{tags_str}。
            请以此情景，在唐宋诗词库中匹配一首最契合的诗词，并从{target_phase}的难度维度进行意境赏析。
            """
        return prompt