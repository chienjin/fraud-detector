from fraud_detector.domain.models import AnalysisResult, Post
from fraud_detector.services.ports import TextAnalyzer


def run_analysis(post: Post, analyzer: TextAnalyzer) -> AnalysisResult:
    return analyzer.analyze(post)
