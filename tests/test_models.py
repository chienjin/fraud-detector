import pytest

from fraud_detector.domain.models import AnalysisResult, RiskLevel


@pytest.mark.parametrize(
    ("post_id", "risk_level", "reasons", "confidence"),
    [
        ("1", RiskLevel.LOW, ["a"], -0.1),
        ("2", RiskLevel.MEDIUM, ["b"], 1.1),
    ],
)
def test_confidence_out_of_range_raises_value_error(
    post_id: str, risk_level: RiskLevel, reasons: list[str], confidence: float
) -> None:
    with pytest.raises(ValueError):
        AnalysisResult(post_id, risk_level, reasons, confidence)


@pytest.mark.parametrize(
    ("post_id", "risk_level", "reasons", "confidence"),
    [
        ("1", RiskLevel.LOW, ["a"], 0.1),
        ("2", RiskLevel.MEDIUM, ["b"], 0),
        ("3", RiskLevel.MEDIUM, ["c"], 1),
    ],
)
def test_valid_confidence_is_kept(
    post_id: str, risk_level: RiskLevel, reasons: list[str], confidence: float
) -> None:
    a = AnalysisResult(post_id, risk_level, reasons, confidence)
    assert a.confidence == confidence
