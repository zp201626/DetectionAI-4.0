import os
from langchain_openai import OpenAIEmbeddings


model = OpenAIEmbeddings(
    api_key=os.environ["INTERNAL_LLM_API_KEY"],
    base_url=os.environ["INTERNAL_LLM_BASE_URL"],
    model=os.environ["INTERNAL_EMBEDDING_MODEL"],
)

# 不用invoke stream
# embed_query、embed_documents
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你", "我稀饭你", "晚上吃啥"]))
