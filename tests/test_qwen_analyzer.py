import json

import pytest

from fraud_detector.adapters.qwen_analyzer import parse_llm_response
from fraud_detector.domain.errors import AnalysisFailedError
from fraud_detector.domain.models import RiskLevel

VALID_RESPONSE = '{"risk_level": "high", "reasons": ["含可疑關鍵字"], "confidence": 0.9}'
BROKEN_RESPONSE = '{"risk_level": "high"'


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
