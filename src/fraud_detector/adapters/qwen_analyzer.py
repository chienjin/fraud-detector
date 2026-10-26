import json

from fraud_detector.domain.errors import AnalysisFailedError
from fraud_detector.domain.models import AnalysisResult, RiskLevel


def parse_llm_response(raw: str, post_id: str) -> AnalysisResult:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise AnalysisFailedError(f"LLM 回傳的格式不是合法的 JSON post_id={post_id}") from e

    return AnalysisResult(
        post_id,
        RiskLevel(data["risk_level"]),
        data["reasons"],
        data["confidence"],  # 從 data 取出 risk_level、reasons、confidence，建立 AnalysisResult
    )
