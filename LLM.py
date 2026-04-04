import os
from openai import OpenAI
import streamlit as st

class LLMEngine:
    def __init__(self, api_key):
        print("Initializing LLM Engine...")
        self.client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        self.model = "moonshot-v1-8k"

    def generate_poetry_content(self, tags):
            # 防御逻辑System Prompt，防止刁难
            system_prompt = (
                "你是一位深谙幽默的国学导师。请根据我提供的意象标签作答：\n"
                "1. 【常规模式】如果标签是纯古风（如山水、明月），请匹配契合的古诗并提供约150字优美赏析。\n"
                "2. 【防御模式】如果标签中出现“跑车、奥特曼、机甲、电子产品、大厦、动漫”等现代或科幻词汇，"
                "说明有看客在开玩笑。请勿崩溃，也不要生硬拒绝，而是用极其幽默的古风口吻调侃这件“现代奇物”，"
                "并为它强行赋一首带有武侠或仙侠色彩的打油诗（如将跑车比作‘钢铁汗血马’，将奥特曼比作‘光之游侠’）。"
            )
            tag_str = "、".join(tags)
            user_prompt = f"当前识图提取的意象为：【{tag_str}】。请先生过目并点评。"

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    stream=True,
                    timeout=15
                )

                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content

            except Exception as e:
                print(f"[ERROR] API Link Failed: {e}")
                yield "\n网络微恙。荐《江雪》一首：千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。————柳宗元"

    def chat_with_memory(self, messages):
        sys_msg = {"role": "system",
                   "content": "你是一位深谙幽默的国学导师。请根据上下文解答学子的追问，保持高雅、鼓励且幽默的口吻。"}
        full_msgs = [sys_msg] + messages
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_msgs,
                stream=True,
                timeout=15
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"\n【导师闭关中】不便对谈（{e}）"


if __name__ == "__main__":
    TEST_KEY= st.secrets["KIMI_API_KEY"]
    engine = LLMEngine(TEST_KEY)
    test_tags = ["山水", "古寺"]

    print("流式响应测试中:\n")
    for word in engine.generate_poetry_content(test_tags):
        print(word, end="", flush=True)
    print("\n\n演示结束。")