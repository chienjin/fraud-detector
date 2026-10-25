import pytest

from fraud_detector.domain.models import RiskLevel
from fraud_detector.domain.scoring import assess_risk,risk_score


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

@pytest.mark.parametrize(
    ("reasons", "expected"),
    [
        (None, 0),
        ([], 0),
        (["aa"], 10),
        (["aa","aaa","aaaa"], 30),
    ],
)
def test_risk_score(reasons:list[str], expected: int) -> None:
     assert risk_score(reasons) == expected
