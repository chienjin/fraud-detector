import logging
import os
from datetime import UTC, datetime

from fraud_detector.domain.models import AnalysisResult, Post, RiskLevel
from fraud_detector.services.analysis import run_analysis


def setup_logging() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


class DemoAnalyzer:
    """暫時的示範用分析器。後端課做出 API 和 KeywordAnalyzer 之後就會移除。"""

    def analyze(self, post: Post) -> AnalysisResult:
        return AnalysisResult(
            post.id, RiskLevel.LOW, ["a"], 0.5
        )  # 回傳一個固定的 AnalysisResult，post_id 用 post.id


def main() -> None:
    setup_logging()
    post = Post(
        "1", "a", ["a.jpg"], datetime(2026, 10, 25, tzinfo=UTC)
    )  # 建立一則 Post，用 DemoAnalyzer 跑 run_analysis
    analyzer = DemoAnalyzer()
    run_analysis(post, analyzer)
