import logging

from fraud_detector.domain.models import AnalysisResult, Post
from fraud_detector.services.ports import TextAnalyzer

logger = logging.getLogger(__name__)


def run_analysis(post: Post, analyzer: TextAnalyzer) -> AnalysisResult:
    logger.info("開始分析貼文 post_id=%s", post.id)
    result = analyzer.analyze(post)
    logger.info("分析完成 post_id=%s risk=%s", post.id, result.risk_level.value)
    return result
