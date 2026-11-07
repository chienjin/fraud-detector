import logging
import os
from datetime import UTC, datetime

from fraud_detector.adapters.keyword_analyzer import KeywordAnalyzer
from fraud_detector.domain.models import Post
from fraud_detector.services.analysis import run_analysis


def setup_logging() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def main() -> None:
    setup_logging()
    post = Post(
        "1", "a", ["a.jpg"], datetime(2026, 10, 25, tzinfo=UTC)
    )  # 建立一則 Post，用 DemoAnalyzer 跑 run_analysis
    analyzer = KeywordAnalyzer()
    run_analysis(post, analyzer)
