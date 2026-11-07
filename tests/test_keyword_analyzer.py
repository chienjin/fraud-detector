from dataclasses import replace

import pytest

from fraud_detector.adapters.keyword_analyzer import KeywordAnalyzer
from fraud_detector.domain.models import Post, RiskLevel

ALL_KEYWORDS_TEXT = "保證獲利 穩賺 加LINE 限時 匯款"


@pytest.mark.parametrize(
    ("text", "expected_risk", "expected_reason_count"),
    [
        ("今天天氣很好", RiskLevel.LOW, 0),
        ("保證獲利，快加LINE", RiskLevel.LOW, 2),
        (ALL_KEYWORDS_TEXT, RiskLevel.MEDIUM, 5),
        (f"{ALL_KEYWORDS_TEXT} https://x.co", RiskLevel.HIGH, 5),
    ],
)
def test_keyword_analyzer_assesses_risk(
    sample_post: Post, text: str, expected_risk: RiskLevel, expected_reason_count: int
) -> None:
    post = replace(sample_post, text=text)

    result = KeywordAnalyzer().analyze(post)

    assert result.post_id == post.id
    assert result.risk_level is expected_risk
    assert len(result.reasons) == expected_reason_count
