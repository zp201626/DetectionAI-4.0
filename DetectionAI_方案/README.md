# DetectionAI 助手实施方案

面向 DRAM Detection 工程师的知识检索与参数推荐方案。用户输入产品结构、工艺 Layer、DOI（Defect of Interest）和候选机台后，系统检索受控知识库、判断机台适配性，再生成**候选检测方向和待验证参数范围**。

> 重要：输出不是经过 qualification 的正式 Recipe。没有内部能力数据、历史 Recipe 或缺少 DOI 类型/尺寸时，系统必须明确返回“信息不足/需要 qualification”，不能让模型猜数值。SP 机台不在本方案范围内。

## 目录

- [`docs/architecture.md`](docs/architecture.md)：节点结构、模块职责、输入输出和流程
- [`prompts/prompts.md`](prompts/prompts.md)：各大模型节点可直接复制的提示词
- [`schemas/request-response.json`](schemas/request-response.json)：请求、检索证据和响应 JSON 示例
- [`plugins/detectionai_plugins.py`](plugins/detectionai_plugins.py)：插件 API 示例（FastAPI），需替换为内部数据库/飞书多维表
- [`plugins/requirements.txt`](plugins/requirements.txt)：插件运行依赖
- [`data/example_machine_capabilities.json`](data/example_machine_capabilities.json)：脱敏示例，仅用于联调
- [`data/example_test_cases.json`](data/example_test_cases.json)：验收测试用例
- [`docs/deployment.md`](docs/deployment.md)：Coze 接入、权限和上线检查清单

## 支持机台

当前范围：`eScan`、`460`、`430`、`BF`、`F300`。`SP` 明确排除。机台的检测原理、DOI 尺寸能力、位置限制和已验证 Recipe 必须来自内部受控数据，不能用公开论文替代。

## 推荐原则

1. Layer 提供工艺和结构背景；DOI 类型、尺寸、位置决定检测物理需求。
2. 论文只解释通用检测原理；内部机台能力和 qualification 数据决定是否可执行。
3. 新 Layer 只能引用相似 Layer 作为候选范围，并标记为 `needs_qualification`。
4. 任何超出历史范围、缺少 DOI 关键字段或与机台原理冲突的结果，都必须降级为人工确认。
5. 最终输出要包含依据、置信度、限制、验证计划、defect owner 待确认问题和 SOP 链接（如已找到）。

## 快速启动插件示例

```powershell
cd DetectionAI_方案/plugins
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn detectionai_plugins:app --reload --port 8000
```

示例 API 仅用于验证 Chatflow 的 HTTP 调用链路，不能直接用于生产。生产环境应接入公司认证、审计、内部数据库和飞书权限控制。
