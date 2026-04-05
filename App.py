import streamlit as st
from PIL import Image
from clip_engine import VisionEngine
from LLM import LLMEngine
from tts_module import text_to_speech
from image_processor import apply_ink_filter
from rag_engine import RAGEngine
from postcard_generator import PostcardGenerator
from map_engine import generate_poet_map
import plotly
from report_engine import ReportEngine

st.set_page_config(page_title="文韵流芳", layout="wide")

import streamlit as st


def inject_custom_css():
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&family=Ma+Shan+Zheng&display=swap');

    html, body, .stApp {
        font-family: 'ZCOOL XiaoWei', 'Ma Shan Zheng', 'KaiTi', 'STKaiti', serif !important;
    }

    * {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="6" fill="%23b23c1c" stroke="%23d4af37" stroke-width="1" opacity="0.8"/><circle cx="8" cy="8" r="2" fill="white" opacity="0.6"/></svg>') 10 10, auto;
    }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: 
            repeating-linear-gradient(45deg, rgba(180, 150, 110, 0.03) 0px, rgba(180, 150, 110, 0.03) 2px, transparent 2px, transparent 8px),
            repeating-linear-gradient(135deg, rgba(130, 100, 70, 0.02) 0px, rgba(130, 100, 70, 0.02) 1px, transparent 1px, transparent 6px),
            linear-gradient(145deg, #f7efdf 0%, #efe0cd 100%);
        background-blend-mode: overlay;
    }

    .stApp {
        filter: url(#agedPaper);
        background-image: none !important;
        background-color: transparent !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(242, 234, 218, 0.92) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(139, 115, 85, 0.4);
        box-shadow: 6px 0 20px rgba(0, 0, 0, 0.08);
    }
    section[data-testid="stSidebar"] * {
        font-family: 'ZCOOL XiaoWei', 'Ma Shan Zheng', 'KaiTi', serif;
    }

    .main > div {
        border: 2px solid transparent;
        border-image: repeating-linear-gradient(
            45deg, 
            #8b5a2b, #b87c4f 15px, 
            #e3c194 20px, #b87c4f 25px, 
            #8b5a2b 35px
        ) 30 stretch;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(250, 245, 235, 0.4);
        border-radius: 0px !important;
    }

    [data-testid="column"] {
        border-right: 1px dashed #c6ad7a;
    }
    [data-testid="column"]:last-child {
        border-right: none;
    }

    .stButton > button, button[kind="secondary"], button[kind="primary"] {
        background-color: #b23c1c !important;
        color: #fef0da !important;
        border: 1px solid #d9b48b !important;
        border-radius: 0px !important;
        font-family: 'ZCOOL XiaoWei', serif !important;
        font-size: 1rem !important;
        padding: 0.4rem 1.2rem !important;
        letter-spacing: 2px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,200,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover, button[kind="secondary"]:hover {
        background-color: #962e12 !important;
        box-shadow: 
            0 0 6px rgba(0,0,0,0.3),
            0 0 15px rgba(0,0,0,0.2),
            0 0 30px rgba(90,40,10,0.2),
            inset 0 0 8px rgba(255,200,100,0.6);
        transform: scale(1.02);
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="%23b23c1c" stroke="%23ffd966" stroke-width="1.5"/><circle cx="9" cy="9" r="2.5" fill="white" opacity="0.9"/></svg>') 12 12, pointer;
    }
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0) 80%);
        transform: translate(-50%, -50%) scale(0);
        transition: transform 0.4s ease-out;
        border-radius: 50%;
        pointer-events: none;
    }
    .stButton > button:hover::after {
        transform: translate(-50%, -50%) scale(2.5);
        opacity: 1;
    }

    [data-testid="stChatMessage"]:first-of-type [data-testid="stChatMessageContent"] {
        writing-mode: vertical-rl;
        text-orientation: mixed;
        height: 380px;
        overflow-x: auto;
        overflow-y: hidden;
        white-space: nowrap;
        background: rgba(235, 220, 195, 0.2);
        padding: 1.2rem 0.8rem;
        border-left: 4px solid #b87c4f;
        border-right: 4px solid #b87c4f;
        box-shadow: inset 0 0 20px rgba(100, 60, 20, 0.1), 0 4px 12px rgba(0,0,0,0.1);
        font-size: 1.15rem;
        line-height: 1.8;
        letter-spacing: 0.1em;
        scrollbar-width: thin;
        scrollbar-color: #b87c4f #ecd9b4;
    }
    [data-testid="stChatMessage"]:first-of-type [data-testid="stChatMessageContent"]::-webkit-scrollbar {
        height: 6px;
        background: #ecd9b4;
    }
    [data-testid="stChatMessage"]:first-of-type [data-testid="stChatMessageContent"]::-webkit-scrollbar-thumb {
        background: #b87c4f;
        border-radius: 3px;
    }

    [data-testid="stChatMessageContent"] {
        font-family: 'ZCOOL XiaoWei', serif;
        background: rgba(250, 242, 228, 0.5);
        border-radius: 0px;
        padding: 0.5rem 1rem;
    }

    @keyframes brushReveal {
        0% {
            mask-image: linear-gradient(to right, transparent 0%, black 0%);
            -webkit-mask-image: linear-gradient(to right, transparent 0%, black 0%);
            opacity: 0.3;
        }
        100% {
            mask-image: linear-gradient(to right, black 100%, transparent 100%);
            -webkit-mask-image: linear-gradient(to right, black 100%, transparent 100%);
            opacity: 1;
        }
    }
    [data-testid="stChatMessage"] {
        animation: brushReveal 0.8s cubic-bezier(0.22, 0.88, 0.36, 1) forwards;
        transform-origin: left;
    }
    .stMarkdown, .stChatMessageContent p {
        animation: brushReveal 0.6s ease-out forwards;
    }

    .stRadio > div, .stSelectSlider {
        background: rgba(210, 180, 140, 0.2);
        padding: 0.3rem;
        border-radius: 0px;
    }
    [data-testid="stFileUploader"] {
        border: 1px dashed #b87c4f;
        background: rgba(245, 235, 215, 0.5);
    }
    .stChatInputContainer textarea, .stTextInput input {
        background: rgba(252, 248, 235, 0.9);
        border: 1px solid #c6ad7a;
        border-radius: 0px;
        font-family: 'Ma Shan Zheng', monospace;
    }
    .stDownloadButton button {
        background-color: #6f4e2e !important;
        border: 1px solid #deb887 !important;
    }
    hr {
        border-top: 2px solid #d2b48c;
        border-image: repeating-linear-gradient(90deg, #b87c4f, #ecd9b4, #b87c4f) 1;
        height: 2px;
    }
    [data-testid="stSlider"] {
        color: #5c3a21;
    }
    </style>
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="position: fixed; top: 0; left: 0; width: 0; height: 0; pointer-events: none;">
        <filter id="agedPaper" x="0" y="0" width="100%" height="100%">
            <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="4" result="noise" />
            <feColorMatrix type="matrix" values="1 0 0 0 0  0 0.95 0 0 0  0 0.85 0 0 0  0 0 0 0.15 0" in="noise" result="coloredNoise" />
            <feBlend in="SourceGraphic" in2="coloredNoise" mode="multiply" />
        </filter>
    </svg>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "postcard_bytes" not in st.session_state:
    st.session_state.postcard_bytes = None


@st.cache_resource
def init_engines():
    return VisionEngine(), LLMEngine(), RAGEngine()


v_engine, l_engine, r_engine = init_engines()

with st.sidebar:
    st.title("教学大脑配置")
    target_phase = st.select_slider(
        "选择当前受教学段",
        options=["小学", "初中", "高中"],
        value="初中"
    )
    st.success(f"当前模式：{target_phase}语文教学")

st.title("文韵流芳 —— 古诗词意境识别系统")

col1, col2 = st.columns([1, 1], gap="large")
st.markdown("""
    <div style="background-color: rgba(139, 115, 85, 0.1); padding: 15px; border-radius: 10px; border-left: 5px solid #8b7355;">
        <b>项目愿景：</b> 以 AI 视觉捕捉山川之美，以时空图谱重塑诗词记忆。
        在这里，每一张照片都是通往盛唐宋元的入口。
    </div>
""", unsafe_allow_html=True)

with col1:
    st.subheader("取景观意")
    input_mode = st.radio("获取画作方式", ["📂 本地上传", "📷 现场取景"], horizontal=True)

    up_file = None
    if input_mode == "📂 本地上传":
        up_file = st.file_uploader("呈上画作（支持 JPG/PNG）", type=["jpg", "jpeg", "png"])
    else:
        st.info("提示：请将镜头对准风景、古物或教材相关画面，获取最佳解析。")
        up_file = st.camera_input("启动意境捕捉仪", label_visibility="collapsed")

    if up_file:
        temp_path = "temp.jpg"
        with open(temp_path, "wb") as f:
            f.write(up_file.getbuffer())

        if st.session_state.current_image != up_file.name:
            st.session_state.messages = []
            st.session_state.current_image = up_file.name
            st.session_state.audio_path = None
            st.session_state.postcard_bytes = None

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
        if len(st.session_state.messages) == 0:
            with st.spinner("凝神观画与翻阅大纲中..."):
                try:
                    with st.spinner("凝神观画中..."):
                        res = v_engine.detect_tags(temp_path)
                        if res and isinstance(res, list):
                            tags = [item['label'] for item in res][:4]
                        else:
                            tags = ["风光", "意境", "古韵"]
                except Exception as e:
                    st.error("画面意境过于深奥，暂时无法参透，请换一张画作试试。")
                    st.stop()

                st.success(f" 观得意象：{' | '.join(tags)}")

                matched_poem = r_engine.retrieve_poem(tags, target_phase)
                if matched_poem:
                    st.info(f"成功锚定【{target_phase}】教材：《{matched_poem['title']}》")
                else:
                    st.info("☁️ 启用云端大模型自由推演")

                final_prompt = r_engine.build_prompt(tags, target_phase, matched_poem)

            st.divider()
            st.markdown("##### 诗境解析")
            chat_box = st.empty()
            full_text = ""

            with st.spinner("挥毫泼墨中..."):
                for chunk in l_engine.generate_poem_analysis(final_prompt):
                    full_text += chunk
                    chat_box.markdown(full_text + "▌")
                chat_box.markdown(full_text)

            st.session_state.messages.append({"role": "assistant", "content": full_text})

            if matched_poem:
                st.divider()
                st.subheader("诗人行迹地图")
                poet_name = matched_poem['author']

                map_fig = generate_poet_map(poet_name)

                if map_fig:
                    st.plotly_chart(map_fig, use_container_width=True)
                    st.caption(f"图中展示了【{poet_name}】一生的迁徙路径，当前作品创作于图中高亮位置。")

            st.divider()
            st.subheader("名家跨时空评教")
            tab1, tab2, tab3 = st.tabs(["苏轼点评", "李清照点评", "王国维点评"])

            with tab1:
                if st.button("请苏子指教"):
                    chat_box_su = st.empty()
                    full_su = ""
                    for chunk in l_engine.generate_expert_critique("苏轼", full_text):
                        full_su += chunk
                        chat_box_su.markdown(full_su + "▌")
                    chat_box_su.markdown(full_su)

            with tab2:
                if st.button("请易安指教"):
                    chat_box_li = st.empty()
                    full_li = ""
                    for chunk in l_engine.generate_expert_critique("李清照", full_text):
                        full_li += chunk
                        chat_box_li.markdown(full_li + "▌")
                    chat_box_li.markdown(full_li)

            with tab3:
                if st.button("请静安指教"):
                    chat_box_wang = st.empty()
                    full_wang = ""
                    for chunk in l_engine.generate_expert_critique("王国维", full_text):
                        full_wang += chunk
                        chat_box_wang.markdown(full_wang + "▌")
                    chat_box_wang.markdown(full_wang)


            st.divider()
            st.subheader(" 研学成果固化")
            if st.button(" 预生成学术研学报告"):

                report_data = {
                    "title": matched_poem['title'] if matched_poem else "意境推演",
                    "content": st.session_state.messages[0]["content"] if st.session_state.messages else "暂无内容",
                    "critiques": {
                        "苏轼": st.session_state.su_critique,
                        "李清照": st.session_state.li_critique,
                        "王国维": st.session_state.wang_critique
                    }
                }

                try:
                    pdf_engine = ReportEngine()
                    pdf_bytes = pdf_engine.generate_pdf(report_data)

                    st.download_button(
                        label="点击下载 PDF 研学报告",
                        data=pdf_bytes,
                        file_name=f"研学报告_{report_data['title']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("报告已生成，请点击上方按钮下载。")
                except Exception as e:
                    st.error(f"PDF生成失败，请检查字体文件是否存在: {e}")

            with st.spinner("寻找声带中..."):
                st.session_state.audio_path = text_to_speech(full_text[:200])

            with st.spinner("封装研学明信片中..."):
                try:
                    pg = PostcardGenerator(font_name="NotoSerifSC-Regular.otf")
                    p_title = matched_poem['title'] if matched_poem else "诗境推演"
                    p_author = matched_poem['author'] if matched_poem else "AI赋诗"
                    _, img_bytes = pg.generate(temp_path, p_title, p_author, full_text, target_phase)
                    st.session_state.postcard_bytes = img_bytes
                except Exception as e:
                    st.error(f"明信片封装失败: {e}")

        else:
            st.success("观得意象已锁定")
            st.divider()
            st.markdown("##### 诗境解析")
            st.markdown(st.session_state.messages[0]["content"])

        if st.session_state.audio_path:
            st.audio(st.session_state.audio_path, format="audio/mp3")

        if st.session_state.postcard_bytes:
            st.download_button(
                label="领取专属研学明信片",
                data=st.session_state.postcard_bytes,
                file_name="文韵流芳_研学明信片.png",
                mime="image/png",
                use_container_width=True
            )

        st.divider()
        st.markdown("##### 探讨与追问")

        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if query := st.chat_input("先生，此句何解？"):
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                ans_box = st.empty()
                full_ans = ""
                for chunk in l_engine.chat_with_memory(st.session_state.messages, target_phase):
                    full_ans += chunk
                    ans_box.markdown(full_ans + "▌")
                ans_box.markdown(full_ans)

            st.session_state.messages.append({"role": "assistant", "content": full_ans})
    else:
        st.info("左侧悬挂画卷，即可听取古音。")
