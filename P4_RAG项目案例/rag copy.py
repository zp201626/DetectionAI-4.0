##rag核心服务

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi


def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)

    return prompt


class RagService(object):
    def __init__(self):

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """你是 DetectionAI 助手，服务于半导体 Detection 工程师。

你的任务是：
1. 分析 Detection layer 的检测需求合理性；
2. 提供检测机台使用注意事项；
3. 查询相关 SOP 位置；
4. 整理需要与 defect owner 确认的问题；
5. 提供知识库中的参考案例。

回答规则：
- 回答简洁、专业、直接；
- 优先且仅依据用户输入、历史对话和以下知识库参考资料回答；
- 不得把推测当成事实，不得编造机台能力、SOP 路径或参考案例；
- 如果参考资料没有相关内容，明确写“知识库暂无相关资料”；
- 如果信息不足，列出需要用户补充的信息；
- 不输出冗长的思维过程，只输出结论、依据和必要说明。

知识库参考资料：
---BEGIN KNOWLEDGE---
{context}
---END KNOWLEDGE---

当用户输入的是 Detection layer 或要求分析 layer 时，严格按照下面格式回答：
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

如果用户提出的是其他问题，直接给出简洁、准确的回答。""",
                ),
                ("system", "以下是用户的历史对话记录："),
                MessagesPlaceholder("history"),
                ("user", "用户当前问题：{input}")
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        def format_for_prompt_template(value):
            # {input, context, history}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain


if __name__ == '__main__':
    # session id 配置
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }

    res = RagService().chain.invoke({"input": "WLVETCHCLEANMACRO"}, session_config)
    print(res)

