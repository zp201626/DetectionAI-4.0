# Coze 接入与上线检查

## 知识库

建议拆成四个知识库：

1. DRAM 产品结构与 Layer 工艺；
2. DOI 分类、检测物理原理和量测定义；
3. 机台能力、限制和已批准 Recipe（内部权限）；
4. 历史缺陷案例、qualification 报告和公开论文索引。

论文应保留题名、DOI、摘要和许可信息；不要把版权受限全文公开上传。所有内部文档按项目/产品/角色做权限过滤。

## Coze 节点配置

- LLM 节点：把 `prompts/prompts.md` 中对应内容放入系统提示词，要求 JSON 输出并开启结构化校验。
- HTTP 插件：分别配置 `/query_machine_capability`、`/evaluate_doi_machine_fit`、`/search_recipe_history`、`/find_sop_document`、`/validate_recipe_recommendation`；请求体使用 `schemas/request-response.json` 的字段。
- 知识库检索：按 Layer、DOI 类型/尺寸、机台和项目过滤，不做无权限的全库暴露。
- 最终 LLM：只消费检索证据和插件返回值；工具失败时报告“数据源不可用”，不能自行补全。

## 上线前检查

- [ ] 所有机台能力和 Recipe 数据有负责人、版本号、更新时间和 qualification 状态。
- [ ] API Key、飞书 token、数据库密码均使用 Coze 密钥/环境变量，未写入代码或 Git。
- [ ] 插件启用 HTTPS、鉴权、超时、重试上限、请求审计和脱敏日志。
- [ ] 对 SP、缺少 DOI 尺寸、越界参数、无权限 SOP、相似 Layer 分别做阻断测试。
- [ ] 由 Detection 工程师和 defect owner 用 `data/example_test_cases.json` 扩展验收集，并批准量产边界。
