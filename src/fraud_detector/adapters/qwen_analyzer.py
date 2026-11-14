import json

from fraud_detector.domain.errors import AnalysisFailedError
from fraud_detector.domain.models import AnalysisResult, RiskLevel


def parse_llm_response(raw: str, post_id: str) -> AnalysisResult:
    try:
        data = json.loads(raw)
        return AnalysisResult(
            post_id=post_id,
            risk_level=RiskLevel(data["risk_level"]),
            reasons=data["reasons"],
            confidence=data[
                "confidence"
            ],  # 從 data 取出 risk_level、reasons、confidence，建立 AnalysisResult
        )
    except (KeyError, TypeError, ValueError) as e:
        raise AnalysisFailedError(f"無法解析 LLM 的回傳內容 post_id={post_id}") from e
