"""使用 OpenAI 兼容接口实现 DetectionAI 的历史消息会话。

本文件对应 LangChain 中的：
    ChatPromptTemplate.from_messages(...)
    MessagesPlaceholder("history")

OpenAI SDK 没有同名的 ChatPromptTemplate 类，直接使用 messages 列表
保存 system、user、assistant 消息即可实现相同效果。
"""

import os

from openai import OpenAI


MODEL_NAME = os.getenv("DASHSCOPE_MODEL", "qwen3-max")

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


SYSTEM_PROMPT = """你是 DetectionAI 助手，服务于 Detection 工程师。
回答必须简洁、专业、直接。

当用户输入 Detection layer 时，请尽量按照以下五项回答：
1. 检测需求是否合理；
2. 所用机台使用注意事项；
3. SOP 位置；
4. 需要和 defect owner 沟通的问题；
5. 参考案例。

优先依据用户提供的信息和知识库回答，不得编造不存在的资料。
如果资料不足，请明确写“知识库暂无相关资料”，并列出需要补充的信息。
"""


def build_messages(history: list[dict[str, str]], user_input: str) -> list[dict[str, str]]:
    """构造本次请求的消息列表。

    这相当于 LangChain 的 MessagesPlaceholder("history")：
    system提示词 + 历史消息 + 当前用户问题。
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_input},
    ]


def ask_detection_ai(history: list[dict[str, str]], user_input: str) -> str:
    """调用模型，并返回本轮回答。"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=build_messages(history, user_input),
    )
    return response.choices[0].message.content or ""


def main() -> None:
    # history 只保存 user 和 assistant 消息；system 提示词每次请求都固定加入。
    history: list[dict[str, str]] = []

    print("DetectionAI 已启动，输入 q 退出。")
    while True:
        user_input = input("\n请输入问题：").strip()
        if user_input.lower() == "q":
            print("DetectionAI 已退出。")
            break
        if not user_input:
            print("问题不能为空。")
            continue

        answer = ask_detection_ai(history, user_input)
        print(f"\nDetectionAI：{answer}")

        # 将本轮对话加入历史，下一轮问题就能参考前文。
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
