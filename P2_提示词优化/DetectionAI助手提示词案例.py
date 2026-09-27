"""DetectionAI 助手提示词优化案例。

本案例将 P2 中的几种提示词方法组合起来：
1. 意图分类：判断用户是在分析 layer，还是提出其他问题；
2. JSON 信息抽取：解析项目、产品、layer、机台等字段；
3. 知识库约束：只依据检索到的资料回答，不编造 SOP 和案例；
4. 固定格式输出：让回答稳定，方便后续接入前端或系统。

运行前请配置 DASHSCOPE_API_KEY，或使用 OpenAI 兼容接口支持的环境变量。
"""

import json
import os
from typing import Any

from openai import OpenAI


MODEL_NAME = os.getenv("DASHSCOPE_MODEL", "qwen3-max")

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
)


DETECTIONAI_SYSTEM_PROMPT = """你是 DetectionAI 助手，服务于半导体 Detection 工程师。

你的任务是：
1. 分析 Detection layer 的检测需求合理性；
2. 提供检测机台使用注意事项；
3. 查询相关 SOP 位置；
4. 整理需要与 defect owner 确认的问题；
5. 提供知识库中的参考案例。

回答规则：
- 简洁、专业、直接；
- 优先依据用户输入和知识库资料；
- 不得把推测当成事实；
- 不得编造机台能力、SOP 路径或参考案例；
- 知识库没有相关内容时，明确回答“知识库暂无相关资料”；
- 信息不足时，列出需要用户补充的信息；
- 不输出冗长的思维过程，只输出结论、依据和必要说明。
"""


def ask_model(messages: list[dict[str, str]]) -> str:
    """调用模型并返回文本结果。"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def classify_intent(question: str) -> str:
    """使用分类提示词识别用户意图。"""
    prompt = """请将用户问题分类为以下类别之一：
[
  "layer_analysis",
  "machine_usage",
  "sop_lookup",
  "defect_owner_discussion",
  "case_search",
  "other"
]

只输出类别名称，不要解释。
"""
    result = ask_model(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ]
    ).strip()

    valid_intents = {
        "layer_analysis",
        "machine_usage",
        "sop_lookup",
        "defect_owner_discussion",
        "case_search",
        "other",
    }
    return result if result in valid_intents else "other"


def extract_layer_info(question: str) -> dict[str, Any]:
    """从 layer 描述中抽取结构化字段。"""
    schema = {
        "project": "",
        "product": "",
        "layer": "",
        "machine": "",
        "process_requirement": "",
        "missing_information": [],
    }
    prompt = f"""请从用户输入中提取 Detection 信息，并严格输出 JSON。

JSON 字段必须与下面完全一致：
{json.dumps(schema, ensure_ascii=False, indent=2)}

规则：
- 只提取原文明确出现的信息；
- 原文没有提到的字段填写“原文未提及”；
- 不要根据缩写自行猜测；
- 无法确认的信息加入 missing_information；
- 不要输出 Markdown 代码块或额外解释。
"""
    result = ask_model(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ]
    ).strip()

    try:
        parsed = json.loads(result)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # 模型偶尔返回非 JSON 时，保留原始内容，避免程序直接中断。
    return {
        **schema,
        "layer": question,
        "missing_information": ["模型未返回合法 JSON", "原始结果：" + result],
    }


def build_answer(question: str, intent: str, layer_info: dict[str, Any], knowledge_context: str) -> str:
    """根据结构化信息和知识库资料生成最终回答。"""
    user_context = {
        "question": question,
        "intent": intent,
        "layer_info": layer_info,
    }
    prompt = f"""{DETECTIONAI_SYSTEM_PROMPT}

请根据以下用户信息和知识库资料回答问题。

用户信息：
{json.dumps(user_context, ensure_ascii=False, indent=2)}

知识库资料（可能为空）：
---BEGIN KNOWLEDGE---
{knowledge_context or "知识库暂无相关资料"}
---END KNOWLEDGE---

如果用户输入的是 layer，请严格使用以下格式：
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

如果是其他问题，直接给出简洁、准确的回答。
"""
    return ask_model([{"role": "system", "content": prompt}])


def main() -> None:
    print("DetectionAI 助手提示词案例")
    print("1. 输入 Detection layer")
    print("2. 输入其他问题")
    choice = input("请选择：").strip()

    if choice == "1":
        question = input(
            "请输入 layer（例如 DH_167T_WLVETCHCLEANMACRO）："
        ).strip()
        intent = "layer_analysis"
        layer_info = extract_layer_info(question)
    elif choice == "2":
        question = input("请输入其他问题：").strip()
        intent = classify_intent(question)
        layer_info = {}
    else:
        print("请输入 1 或 2。")
        return

    # 实际项目中，这里应替换为 Chroma 等向量库的检索结果。
    knowledge_context = "请在此处放入与当前问题相关的知识库检索结果。"
    answer = build_answer(question, intent, layer_info, knowledge_context)
    print("\nDetectionAI：")
    print(answer)


if __name__ == "__main__":
    main()
