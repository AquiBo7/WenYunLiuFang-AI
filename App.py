import streamlit as st
from PIL import Image
from clip_engine import VisionEngine
from LLM import LLMEngine
from tts_module import text_to_speech
from image_processor import apply_ink_filter

#基础配置
st.set_page_config(page_title="文韵流芳", layout="wide")

#核心状态隔离与记忆初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# 沉浸式古风css
custom_css = """
<style>
    .stApp {
        background-color: #f8f4e6;
        background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAMAAAAp4eJFAAAAVFBMVEUAAADu7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u7u4m1P48AAAAnRSTlMAAAAAAF5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl5eXl7S4VcaAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAWklEQVQ4y+3RMQrAIBBBUUf//+9KIKQRZ8vUgp9i4M4wZid3ZneGR0ZHhodGRkaGh0ZGRoaHRkZGhodeGR0ZHu3YndmZ3RkeGR0ZHhodGRkaGR4ZGRkaGR4ZGRp65R/9zAkXq0fVNAAAAABJRU5ErkJggg==');
        color: #2c2c2c;
        font-family: 'KaiTi', 'STKaiti', 'SimSun', serif;
    }
    [data-testid="stHeader"], footer, #MainMenu {visibility: hidden;}
    [data-testid="stSidebar"] {background-color: transparent !important;}
    h1 {
        color: #5c3a21 !important;
        text-align: center;
        font-family: 'KaiTi', 'STKaiti', serif;
        border-bottom: 2px solid #8b7355;
        padding-bottom: 15px;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h2, h3, h5 { color: #5c3a21 !important; font-family: 'KaiTi', 'STKaiti', serif; }
    [data-testid="stNotification"] {
        background-color: rgba(139, 115, 85, 0.05);
        color: #2c2c2c;
        border: 1px solid rgba(139, 115, 85, 0.2);
        border-radius: 5px;
    }
    [data-testid="stImage"] img {
        border: 10px solid #eaddcf;
        outline: 1px solid #5c3a21;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.2);
        border-radius: 2px;
    }
    .stCheckbox, .stChatInputContainer {
        color: #5c3a21 !important;
        border-color: #8b7355 !important;
    }
    [data-testid="stChatMessageContent"] p, [data-testid="stChatMessageContent"] div {
        color: #2c2c2c !important;
    }
    
    [data-testid="stChatMessage"] {
        background-color: rgba(139, 115, 85, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


@st.cache_resource
def init_engines():
    api_key = st.secrets["KIMI_API_KEY"]
    return VisionEngine(), LLMEngine(api_key)


v_engine, l_engine = init_engines()

st.title("文韵流芳 —— 古诗词意境识别系统")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("取景观意")
    up_file = st.file_uploader("呈上画作（支持 JPG/PNG）", type=["jpg", "jpeg", "png"])

    if up_file:
        temp_path = "temp.jpg"
        with open(temp_path, "wb") as f:
            f.write(up_file.getbuffer())

        #记忆重置：只要换图，立刻清空过往聊天记录
        if st.session_state.current_image != up_file.name:
            st.session_state.messages = []
            st.session_state.current_image = up_file.name
            st.session_state.audio_path = None

        st.markdown("---")
        img_placeholder = st.empty()
        view_mode = st.radio("视界选择", ("原图真迹", "一洗水墨"), horizontal=True)

        if view_mode == "一洗水墨":
            with st.spinner("挥毫泼墨中..."):
                ink_img = apply_ink_filter(temp_path)
                if ink_img:
                    img_placeholder.image(ink_img, caption="墨染山河", use_container_width=True)
                else:
                    st.error("笔墨微干，暂无法化墨。")
        else:
            img_placeholder.image(up_file, caption="待品鉴真迹", use_container_width=True)

with col2:
    st.subheader("先生赋诗")
    if up_file:
        # 首次分析生成
        if len(st.session_state.messages) == 0:
            with st.spinner("凝神观画中..."):
                res = v_engine.detect_tags(temp_path)
                try:
                    if res and isinstance(res, list):
                    tags = [item['label'] for item in res][:3]
                    else:
                        tags = ["风光", "意境", "古韵"] # 如果没识别出来，用通用词兜底
                except Exception as e:
                    print(f"识别标签出错: {e}")
                    tags = ["风光", "意境", "古韵"]
                st.success(f" 观得意象：{' | '.join(tags)}")

            st.divider()
            st.markdown("##### 诗境解析")
            chat_box = st.empty()
            full_text = ""

            with st.spinner("挥毫泼墨中..."):
                for chunk in l_engine.generate_poetry_content(tags):
                    full_text += chunk
                    chat_box.markdown(full_text + "▌")
                chat_box.markdown(full_text)


            st.session_state.messages.append({"role": "assistant", "content": full_text})

            with st.spinner("寻找声带中..."):
                st.session_state.audio_path = text_to_speech(full_text[:200])

        # 记忆回放
        else:
            st.success("观得意象已锁定")
            st.divider()
            st.markdown("##### 诗境解析")
            st.markdown(st.session_state.messages[0]["content"])

        #挂载语音播放器
        if st.session_state.audio_path:
            st.audio(st.session_state.audio_path, format="audio/mp3")

        # 探讨与追问区
        st.divider()
        st.markdown("##### 探讨与追问")

        #遍历跳过第一条的后续聊天记录
        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        #聊天输入框
        if query := st.chat_input("bro，这句诗何解？"):
            #存入用户提问并显示
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            #携带全局记忆向大模型请求
            with st.chat_message("assistant"):
                ans_box = st.empty()
                full_ans = ""
                for chunk in l_engine.chat_with_memory(st.session_state.messages):
                    full_ans += chunk
                    ans_box.markdown(full_ans + "▌")
                ans_box.markdown(full_ans)

            # 存入导师回答
            st.session_state.messages.append({"role": "assistant", "content": full_ans})
    else:
        st.info("左侧悬挂画卷，即可听取古音。")
