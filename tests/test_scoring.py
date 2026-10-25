import pytest

from fraud_detector.domain.models import RiskLevel
from fraud_detector.domain.scoring import assess_risk


@pytest.mark.parametrize(
    ("post_text", "suspicious_keyword_count", "expected"),
    [
        (None, 3, None),
        ("", 3, None),
        ("aa", 3, RiskLevel.LOW),
        ("aa", 4, RiskLevel.MEDIUM),
        ("http://a.com", 4, RiskLevel.HIGH),
    ],
)
def test_assess_risk(
    post_text: str | None, suspicious_keyword_count: int, expected: RiskLevel | None
) -> None:
    assert assess_risk(post_text, suspicious_keyword_count) == expected
