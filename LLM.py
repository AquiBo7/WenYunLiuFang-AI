import os
from openai import OpenAI
import streamlit as st


class LLMEngine:
    def __init__(self):
        print("Initializing LLM Engine...")
        api_key = st.secrets["KIMI_API_KEY"]
        self.client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
        self.model = "moonshot-v1-8k"

    def generate_poem_analysis(self, final_prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个沉浸式大思政文旅助手兼语文教育专家。"},
                    {"role": "user", "content": final_prompt}
                ],
                stream=True,
                timeout=15
            )

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        except Exception as e:
            print(f"API Error: {e}") 
            yield "网络微漾，请稍后再试。暂荐《江雪》代：千山鸟飞绝，万径人踪灭，孤舟蓑笠翁，独钓寒江雪。————柳宗元"

    def chat_with_memory(self, messages, target_phase="初中"):
        sys_msg = {
            "role": "system",
            "content": f"你是一位深谙幽默的{target_phase}语文导师。请根据上下文解答学子的追问，保持高雅、鼓励且幽默的口吻。"
        }
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

    def generate_expert_critique(self, expert_name, poem_content):
        prompts = {
            "苏轼": "你现在是北宋文豪苏东坡。你性格豪放、乐天。请用旷达、洒脱的语气点评这首诗的意境，多谈人生哲学，偶尔用‘老夫’自称。",
            "李清照": "你现在是千古第一才女李清照。你心思细腻，感性婉约。请从情感的浓淡、物哀之美、辞章的工巧角度进行点评，语气要清丽脱俗。",
            "王国维": "你现在是近代美学大师王国维。请引用《人间词话》中‘境界’的理论，点评此诗达到了哪种‘意境’，语气要严谨、富有学术气息。"
        }

        system_prompt = prompts.get(expert_name, "你是一位资深国学专家。")
        user_prompt = f"请先生对这首诗词进行深度点评：\n\n{poem_content}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True
            )
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"先生暂不便指点：{e}"


if __name__ == "__main__":

    engine = LLMEngine()
    test_prompt = "你是一位小学语文老师，请用简单的语言解释‘床前明月光’。"
    print("流式响应测试中:\n")
    for word in engine.generate_poem_analysis(test_prompt):
        print(word, end="", flush=True)
    print("\n\n演示结束。")
