import json

import requests

from fraud_detector.domain.errors import AnalysisFailedError, ExternalServiceUnavailableError
from fraud_detector.domain.models import AnalysisResult, Post, RiskLevel

DEFAULT_TIMEOUT_SECONDS = 10.0
ANALYZE_PATH = "/analyze"


class QwenAnalyzer:
    """呼叫 Qwen 模型伺服器的分析器。"""

    def __init__(
        self,
        base_url: str,
        analyze_path: str = ANALYZE_PATH,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._base_url = base_url
        self._analyze_path = analyze_path
        self.timeout = timeout

    def analyze(self, post: Post) -> AnalysisResult:
        try:
            response = requests.post(
                self._base_url + self._analyze_path, json={"text": post.text}, timeout=self.timeout
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise ExternalServiceUnavailableError(...) from e
        return parse_llm_response(response.text, post.id)


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
