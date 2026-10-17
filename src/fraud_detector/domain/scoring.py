from fraud_detector.domain.models import RiskLevel

SCORE_PER_REASON = 10
SUSPICIOUS_KEYWORD_THRESHOLD = 3


def risk_score(reasons: list[str]) -> int:
    if not reasons:
        return 0
    return len(reasons) * SCORE_PER_REASON


def assess_risk(post_text: str | None, suspicious_keyword_count: int) -> RiskLevel | None:
    if not post_text:
        return None
    if suspicious_keyword_count <= SUSPICIOUS_KEYWORD_THRESHOLD:
        return RiskLevel.LOW
    if "http" not in post_text:
        return RiskLevel.MEDIUM
    return RiskLevel.HIGH
