from fraud_detector.domain.models import AnalysisResult, Post, RiskLevel
from fraud_detector.services.analysis import run_analysis


class FakeAnalyzer:
    def __init__(self, result: AnalysisResult) -> None:
        self.result = result
        self.received_posts: list[Post] = []

    def analyze(self, post: Post) -> AnalysisResult:
        self.received_posts.append(post)
        return self.result


def test_run_analysis_returns_analyzer_result(sample_post: Post) -> None:
    # Arrange
    expected = AnalysisResult(
        post_id=sample_post.id,
        risk_level=RiskLevel.HIGH,
        reasons=["含可疑關鍵字：保證獲利"],
        confidence=0.9,
    )
    analyzer = FakeAnalyzer(expected)

    # Act
    result = run_analysis(sample_post, analyzer)

    # Assert
    assert result is expected
    assert len(analyzer.received_posts) == 1
    assert analyzer.received_posts[0] is sample_post
