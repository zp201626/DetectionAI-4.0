# 知识库更新主程序（Streamlit）
#
# 【在项目虚拟环境中安装依赖】
# 请在项目根目录：
# C:\Users\Maya\Desktop\AI大模型RAG与智能体开发
# 执行：
# .\.venv\Scripts\python.exe -m pip install streamlit langchain-chroma langchain-community dashscope
#
# 【设置阿里云 DashScope API Key】
# 如果运行时提示缺少 API Key，请先执行：
# $env:DASHSCOPE_API_KEY="你的阿里云API_KEY"
#
# 【启动 Streamlit 页面】
# 方式一：在项目根目录直接执行：
# .\.venv\Scripts\python.exe -m streamlit run "P4_RAG项目案例\app_file_uploader.py"
#
# 方式二：先进入当前目录，再执行：
# cd "P4_RAG项目案例"
# ..\.venv\Scripts\python.exe -m streamlit run app_file_uploader.py
#
# 启动成功后，在浏览器打开：http://localhost:8501
#
# 【验证 Streamlit 是否安装成功】
# .\.venv\Scripts\python.exe -c "import streamlit; print(streamlit.__version__)"

"""
基于Streamlit完成WEB网页上传服务

pip install streamlit

Streamlit：当WEB页面元素发生变化，则代码重新执行一遍
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# file_uploader
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,    # False表示仅接受一个文件的上传
)

# session_state就是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024    # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # get_value -> bytes -> decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中。。。"):       # 在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)




