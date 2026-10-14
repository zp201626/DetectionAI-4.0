"""DetectionAI Coze HTTP 插件示例。

这是可联调的安全骨架：示例数据不代表任何真实机台能力。生产环境请替换为
内部认证后的数据库/飞书多维表查询，并增加审计、超时和权限校验。
"""
from typing import Any, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

SUPPORTED = {"eScan", "460", "430", "BF", "F300"}
app = FastAPI(title="DetectionAI plugins", version="0.1.0")

class MachineQuery(BaseModel):
    machine: str

class FitQuery(BaseModel):
    machine: str
    layer: str
    doi_type: list[str] = Field(min_length=1)
    doi_size_value: float | None = Field(default=None, gt=0)
    doi_size_unit: Literal["nm", "um"] | None = None
    doi_location: str | None = None
    doi_electrical: bool = False

class RecipeQuery(BaseModel):
    project: str | None = None
    product: str | None = None
    layer: str
    machine: str
    doi_type: list[str] = Field(default_factory=list)

def check_machine(machine: str) -> None:
    if machine == "SP":
        raise HTTPException(422, "SP 暂不纳入 DetectionAI 方案")
    if machine not in SUPPORTED:
        raise HTTPException(422, f"不支持的机台：{machine}")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/query_machine_capability")
def query_machine_capability(q: MachineQuery) -> dict[str, Any]:
    check_machine(q.machine)
    # TODO: 用内部受控数据源替换；不要把猜测的数值写在这里。
    return {"machine": q.machine, "capability": None,
            "status": "data_source_not_configured",
            "message": "请接入已批准的机台能力库后再进行生产判断"}

@app.post("/evaluate_doi_machine_fit")
def evaluate_doi_machine_fit(q: FitQuery) -> dict[str, Any]:
    check_machine(q.machine)
    if not q.doi_type or q.doi_size_value is None or q.doi_size_unit is None:
        return {"fit_status": "insufficient_information", "reasons": ["DOI 类型和尺寸单位为必填"]}
    return {"fit_status": "insufficient_information",
            "reasons": ["示例插件未接入内部能力库，禁止自动宣称适配"],
            "inputs": q.model_dump()}

@app.post("/search_recipe_history")
def search_recipe_history(q: RecipeQuery) -> dict[str, Any]:
    check_machine(q.machine)
    return {"exact_match": False, "reference_type": "similar_layer",
            "qualification_status": "unknown", "records": [],
            "message": "示例插件未接入历史 Recipe 数据源"}

@app.post("/find_sop_document")
def find_sop_document(q: RecipeQuery) -> dict[str, Any]:
    check_machine(q.machine)
    return {"found": False, "sop_name": None, "sop_url": None,
            "message": "示例插件未接入飞书文档索引；请配置权限后查询"}

@app.post("/validate_recipe_recommendation")
def validate_recipe_recommendation(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("fit_status") in {"not_recommended", "insufficient_information"}:
        return {"decision": "block", "reasons": ["机台适配性不足或信息不完整"]}
    if payload.get("qualification_status") != "qualified":
        return {"decision": "warn", "reasons": ["未完成 qualification，不得直接量产"]}
    return {"decision": "pass", "reasons": []}
