# AI 大模型 RAG 与智能体开发

## 公司内网网关配置

已将原先直连本地 Ollama 的示例改为 OpenAI 兼容网关。运行前请在公司电脑配置以下环境变量：

```powershell
$env:INTERNAL_LLM_BASE_URL="http://公司网关地址/v1"
$env:INTERNAL_LLM_API_KEY="公司网关提供的密钥"
$env:INTERNAL_LLM_MODEL="公司网关中的聊天模型名"
$env:INTERNAL_EMBEDDING_MODEL="公司网关中的向量模型名"
```

网关地址应填写完整的 OpenAI 兼容接口地址（通常以 `/v1` 结尾）。如果网关不需要鉴权，也请按公司要求设置 `INTERNAL_LLM_API_KEY`。

这些变量只对当前终端窗口生效。也可以使用公司统一的环境变量管理方式配置，不要把真实密钥提交到 Git。

对应示例位于 `P2_提示词优化` 和 `P3_LangChainRAG开发` 目录。运行前需要安装 `openai`、`langchain-openai` 及项目实际用到的其他 Python 依赖。
