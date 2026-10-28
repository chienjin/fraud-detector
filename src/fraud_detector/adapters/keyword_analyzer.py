from fraud_detector.domain.models import AnalysisResult, Post, RiskLevel
from fraud_detector.domain.scoring import assess_risk

SUSPICIOUS_KEYWORDS = ("保證獲利", "穩賺", "加LINE", "限時", "匯款")
KEYWORD_CONFIDENCE = 0.5


class KeywordAnalyzer:
    """不需要任何模型的分析器：用關鍵字規則判斷，給展示和測試使用。"""

    def analyze(self, post: Post) -> AnalysisResult:
        reasons = [f"含可疑關鍵字：{word}" for word in SUSPICIOUS_KEYWORDS if word in post.text]
        risk_level = assess_risk(post.text, len(reasons)) or RiskLevel.LOW
        return AnalysisResult(
            post_id=post.id,
            risk_level=risk_level,
            reasons=reasons,
            confidence=KEYWORD_CONFIDENCE,
        )
