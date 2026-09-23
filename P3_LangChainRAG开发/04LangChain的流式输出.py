# from langchain_community.llms.tongyi import Tongyi
#
# model = Tongyi(model="qwen-max")
#
# # 通过stream方法获得流式输出
# res = model.stream(input="你是谁呀能做什么？")
#
# for chunk in res:
#     print(chunk, end="", flush=True)

import os
from langchain_openai import OpenAI

model = OpenAI(
    api_key=os.environ["INTERNAL_LLM_API_KEY"],
    base_url=os.environ["INTERNAL_LLM_BASE_URL"],
    model=os.environ["INTERNAL_LLM_MODEL"],
)

res = model.stream(input="你是谁呀能做什么？")

for chunk in res:
    print(chunk, end="", flush=True)
