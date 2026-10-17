from typing import Protocol

from fraud_detector.domain.models import AnalysisResult, Post


class TextAnalyzer(Protocol):
    def analyze(self, post: Post) -> AnalysisResult: ...
