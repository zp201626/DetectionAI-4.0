# Chatflow 节点与模块设计

## 1. 流程

```text
开始 → 信息抽取 → 意图分流 → 缺失信息判断
     → 并行检索：DRAM结构 / Layer工艺 / DOI原理 / 历史案例 / 论文
     → 查询机台能力 → DOI-机台适配判断
     → 查询历史Recipe → 生成候选参数 → 参数安全校验
     → 查询SOP → 最终报告 → 结束
```

### 节点表

| 节点 | 类型 | 输入 | 输出/关键参数 |
|---|---|---|---|
| 开始 | 用户输入 | `query` | 原始问题 |
| 信息抽取 | LLM+JSON | `query` | `project/product/layer/machine/doi_type/doi_size_value/doi_size_unit/doi_location/structure_description/process_step` |
| 意图分流 | 条件 | 抽取 JSON | `parameter_recommendation`、`sop_lookup`、`general_question` |
| 缺失信息判断 | 条件 | 抽取 JSON | 缺少 DOI 类型或尺寸时停止推荐，仅提出补充问题 |
| 结构/工艺检索 | 知识库 | `product/layer/process_step` | 结构、材料、关键尺寸、工艺风险 |
| DOI/论文检索 | 知识库 | `doi_type/size/location` | 检测原理和适用性证据 |
| 历史案例检索 | 知识库/插件 | `project/product/layer/machine/doi` | exact 或 similar 案例、Recipe、qualification 状态 |
| 查询机台能力 | HTTP 插件 | `machine` | 检测原理、尺寸范围、位置、电性能力、限制 |
| DOI-机台适配 | HTTP 插件 | Layer+DOI+机台能力 | `recommended/partially_recommended/not_recommended/insufficient_information` |
| 生成候选参数 | LLM | 全部检索证据 | 参数候选范围、来源、置信度、风险 |
| 参数校验 | HTTP 插件 | 候选参数+历史范围+适配结论 | `pass/warn/block`，阻止越界和无依据数值 |
| SOP 查询 | HTTP 插件 | 项目/产品/Layer/机台 | 飞书文档名称、版本、`sop_url` |
| 最终报告 | LLM | 上述结构化结果 | 简洁中文报告，禁止伪装为正式 Recipe |

## 2. 字段约束

- `machine` 只能是 `eScan`、`460`、`430`、`BF`、`F300`；输入 `SP` 时返回“不在当前范围”。
- `doi_size_value` 必须为正数，统一换算到 `nm` 或 `um`；没有尺寸不得宣称满足灵敏度。
- `doi_type` 至少包含一种受控枚举：`particle`、`scratch`、`pattern_defect`、`open`、`short`、`contact`、`void`、`unknown`。
- `qualification_status`：`qualified`、`engineering`、`needs_qualification`、`unknown`。
- 新 Layer：`exact_match=false`、`reference_type=similar_layer`，最终结论只能是候选方案。

## 3. 最终报告格式

1. 结论：机台是否适配（以及依据）
2. 候选参数范围：每个参数注明来源、历史范围和置信度
3. 机台注意事项与检测盲区
4. SOP：`[点击打开 SOP](sop_url)`（没有 URL 就写“未找到/需权限”）
5. 需要 defect owner 确认的问题
6. 参考案例/论文
7. 验证计划：wafer 数量、golden sample、灵敏度/误报监控、放行条件

禁止输出：未经数据支持的精确 Recipe、内部凭证、绕过飞书权限的链接、把相似 Layer 当成已认证方案。
