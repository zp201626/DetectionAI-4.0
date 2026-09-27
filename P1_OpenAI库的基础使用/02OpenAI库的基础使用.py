import os
from openai import OpenAI

# 1. 获取client对象，OpenAI类对象
client = OpenAI(
    #api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2. 调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "你是一个DetectionAI助手，并且不说废话简单回答"},
        {"role": "assistant", "content": "好的，我是DetectionAI助手，并且话不多，你要问什么？"},
        {"role": "user", "content": "列举Detection部门常用的机台"}
    ]
)

# 3. 处理结果
print(response.choices[0].message.content)

## 需要先在CMD安装open的包
