## DetectionAI 助手主程序，启动对话 WEB 页面
import time
from rag import RagService
import streamlit as st
import config_data as config

st.set_page_config(page_title="DetectionAI 助手", page_icon="🔍")
st.title("DetectionAI 助手")
st.caption("面向 Detection 工程师的 layer、机台、SOP 和 defect owner 问答助手")
st.divider()

LAYER_ANALYSIS_PROMPT = """请分析 Detection 工程师正在做的 layer，并严格按以下格式回答：

【解析结果】
- 项目：
- 产品：
- Layer：
- 检测机台：

【1. 检测需求合理性】
结论：
依据：

【2. 机台使用注意事项】
- 

【3. SOP位置】
- 

【4. 需要与defect owner确认的问题】
- 

【5. 参考案例】
- 

【信息缺口】
- 

只依据知识库和用户明确提供的信息回答；没有资料时写“知识库暂无相关资料”，不要编造。"""

if "message" not in st.session_state:
    st.session_state["message"] = [
        {
            "role": "assistant",
            "content": (
                "我是 DetectionAI 助手。请选择问题类型：\n\n"
                "1. 输入 Detection 工程师正在做的 layer\n"
                "2. 其他问题"
            ),
        }
    ]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "question_type" not in st.session_state:
    st.session_state["question_type"] = "Layer 分析"

with st.sidebar:
    st.subheader("问题类型")
    st.session_state["question_type"] = st.radio(
        "请选择",
        ["Layer 分析", "其他问题"],
        index=0 if st.session_state["question_type"] == "Layer 分析" else 1,
    )
    if st.button("清空当前会话"):
        st.session_state["message"] = [
            {
                "role": "assistant",
                "content": "会话已清空。请选择 Layer 分析或其他问题。",
            }
        ]
        st.rerun()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面最下方提供用户输入栏
placeholder = (
    "例如：DH_167T_WLVETCHCLEANMACRO，使用 F300 机台"
    if st.session_state["question_type"] == "Layer 分析"
    else "请输入其他 Detection 问题"
)
prompt = st.chat_input(placeholder, key="detection_input")

if prompt:
    if st.session_state["question_type"] == "Layer 分析":
        prompt_for_rag = f"{LAYER_ANALYSIS_PROMPT}\n\n用户输入的 layer：{prompt}"
    else:
        prompt_for_rag = prompt

    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    ai_res_list = []
    with st.spinner("AI思考中..."):
        res_stream = st.session_state["rag"].chain.stream(
            {"input": prompt_for_rag},
            config.session_config,
        )
        # yield

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(str(chunk))
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})

# ["a", "b", "c"]   "".join(list)    -> abc
# ["a", "b", "c"]   ",".join(list)    -> a,b,c
