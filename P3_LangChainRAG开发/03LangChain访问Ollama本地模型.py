import os
from langchain_openai import OpenAI

model = OpenAI(
    api_key=os.environ["INTERNAL_LLM_API_KEY"],
    base_url=os.environ["INTERNAL_LLM_BASE_URL"],
    model=os.environ["INTERNAL_LLM_MODEL"],
)

res = model.invoke(input="你是谁呀能做什么？")

print(res)
