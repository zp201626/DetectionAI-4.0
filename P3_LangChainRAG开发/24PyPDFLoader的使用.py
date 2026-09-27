#需要先安装pyPDF库
#pip install pypdf
#from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader

# loader = PyPDFLoader(
#     file_path="C:\\Users\\Maya\\Desktop\\AI大模型RAG与智能体开发\\P3_LangChainRAG开发\\data\\pdf2.pdf",
#     mode="single",        # 默认是page模式，每个页面形成一个Document文档对象，
#                         # single模式，不管有多少页，只返回1个Document对象
#     password="itheima"
# )

# i = 0
# for doc in loader.lazy_load():
#     i += 1
#     print(doc)
#     print("="*20, i)


from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path=r"C:\Users\Maya\Desktop\AI大模型RAG与智能体开发\P3_LangChainRAG开发\data\pdf2.pdf",
    mode="single",
    password="itheima",
)

for i, doc in enumerate(loader.lazy_load(), start=1):
    print(doc)
    print("=" * 20, i)
