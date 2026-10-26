class FraudDetectorError(Exception):
    """這個專案所有例外的共同父類別。"""


class AnalysisFailedError(FraudDetectorError):
    """貼文分析失敗。"""


class ExternalServiceUnavailableError(FraudDetectorError):
    """外部查核服務無法使用。"""
