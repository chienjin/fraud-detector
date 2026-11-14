import json

import pytest
import requests

from fraud_detector.adapters.qwen_analyzer import QwenAnalyzer, parse_llm_response
from fraud_detector.domain.errors import AnalysisFailedError, ExternalServiceUnavailableError
from fraud_detector.domain.models import Post, RiskLevel

VALID_RESPONSE = '{"risk_level": "high", "reasons": ["含可疑關鍵字"], "confidence": 0.9}'
BROKEN_RESPONSE = '{"risk_level": "high"'

BASE_URL = "http://qwen.test"


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"status={self.status_code}")


def test_valid_response_is_parsed() -> None:
    result = parse_llm_response(VALID_RESPONSE, post_id="p1")

    assert result.post_id == "p1"
    assert result.risk_level is RiskLevel.HIGH
    assert result.reasons == ["含可疑關鍵字"]
    assert result.confidence == 0.9


def test_broken_json_raises_analysis_failed_error() -> None:
    with pytest.raises(AnalysisFailedError):
        parse_llm_response(BROKEN_RESPONSE, post_id="p1")


def test_broken_json_keeps_original_cause() -> None:
    with pytest.raises(AnalysisFailedError) as exc_info:
        parse_llm_response(BROKEN_RESPONSE, post_id="p1")

    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


@pytest.mark.parametrize(
    ("raw", "expected_cause"),
    [
        ("not json", json.JSONDecodeError),
        ('{"risk_level": "low", "confidence": 0.5}', KeyError),
        ('{"risk_level": "extreme", "reasons": ["a"], "confidence": 0.5}', ValueError),
        ('{"risk_level": "low", "reasons": ["a"], "confidence": 1.5}', ValueError),
    ],
)
def test_invalid_response_raises_analysis_failed_error(
    raw: str, expected_cause: type[Exception]
) -> None:
    with pytest.raises(AnalysisFailedError) as exc_info:
        parse_llm_response(raw, post_id="p1")

    assert type(exc_info.value.__cause__) is expected_cause


def test_analyze_returns_result_and_sends_timeout(
    monkeypatch: pytest.MonkeyPatch, sample_post: Post
) -> None:
    calls: list[dict[str, object]] = []

    def fake_post(*args: object, **kwargs: object) -> FakeResponse:
        calls.append(kwargs)  # 記錄收到的參數
        return FakeResponse(VALID_RESPONSE)

    monkeypatch.setattr("fraud_detector.adapters.qwen_analyzer.requests.post", fake_post)

    result = QwenAnalyzer(BASE_URL, timeout=3).analyze(sample_post)

    assert result.post_id == sample_post.id
    assert calls[0]["timeout"] == 3  # 確認 timeout 有傳進去


def test_analyze_timeout_raises_service_unavailable(
    monkeypatch: pytest.MonkeyPatch, sample_post: Post
) -> None:
    def fake_post(*args: object, **kwargs: object) -> FakeResponse:
        raise requests.Timeout  # 丟出 requests.Timeout

    monkeypatch.setattr("fraud_detector.adapters.qwen_analyzer.requests.post", fake_post)

    with pytest.raises(ExternalServiceUnavailableError) as exc_info:  # 預期哪一種例外？
        QwenAnalyzer(BASE_URL).analyze(sample_post)

    assert type(exc_info.value.__cause__) is requests.Timeout  # 原始錯誤是什麼？
