"""DetectionAI 助手：带历史消息的交互式调用示例。"""

from openai import OpenAI


MODEL_NAME = "qwen3-max"

SYSTEM_PROMPT = """你是 DetectionAI 助手，专门帮助 Detection 工程师处理机台和 layer 相关问题。
回答必须简洁、专业、直接，不说客套话，不编造知识库中不存在的信息。

当用户输入一个 layer（例如 DH_167T_WLVETCHCLEANMACRO）时，请严格按下面五项回答：
先识别命名信息：DH 表示项目，167T 表示产品，WLVETCHCLEANMACRO 表示 layer，F300 表示检测机台（若用户提供了机台信息）。
1. 检测需求是否合理：说明判断和理由；
2. 所用机台使用注意事项；
3. SOP 位置；
4. 需要和 defect owner 沟通的问题；
5. 参考案例。

优先依据已接入的知识库回答。如果知识库没有对应资料，请明确写“知识库暂无相关资料”，并指出需要补充什么信息。
"""


def stream_answer(client: OpenAI, messages: list[dict[str, str]]) -> str:
    """流式输出模型回答，并返回完整回答，便于写入历史消息。"""
    response = client.chat.completions.create(
        model="qwen3.8-flash",
        messages=messages,
        stream=True,
    )

    answer_parts: list[str] = []
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            answer_parts.append(content)

    print()
    return "".join(answer_parts)


def ask_layer() -> str:
    """读取 layer；输入 q/Q 可返回上一级菜单。"""
    while True:
        layer = input("请输入 layer（例如 DH_167T_WLVETCHCLEANMACRO，输入 q 返回）：").strip()
        if layer:
            return layer
        print("layer 不能为空，请重新输入。")


def main() -> None:
    client = OpenAI(base_url="https://llm-gny4pxbsrkq9e5ju.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")

    # 保留欢迎语和后续问答，模型可以利用完整的对话历史。
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": (
                "我是 DetectionAI 助手。请选择：\n"
                "1. 输入 Detection 工程师正在做的 layer\n"
                "2. 其他问题"
            ),
        },
    ]

    while True:
        print("\n请选择问题类型：")
        print("1. 输入 Detection 工程师正在做的 layer")
        print("2. 其他问题")
        print("q. 退出")
        choice = input("请输入选项：").strip().lower()

        if choice == "q":
            print("DetectionAI 已退出。")
            break

        if choice == "1":
            user_input = ask_layer()
            if user_input.lower() == "q":
                continue
            prompt = f"请分析 Detection 工程师正在做的 layer：{user_input}"
        elif choice == "2":
            prompt = input("请输入其他问题：").strip()
            if not prompt:
                print("问题不能为空，请重新选择。")
                continue
        else:
            print("请输入 1、2 或 q。")
            continue

        messages.append({"role": "user", "content": prompt})
        print("\nDetectionAI：", end="")
        answer = stream_answer(client, messages)
        messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()