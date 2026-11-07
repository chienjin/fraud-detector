from typing import Self

from pydantic import BaseModel, Field

from fraud_detector.domain.models import AnalysisResult

MAX_TEXT_LENGTH = 5000


class AnalyzePostRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)
    image_urls: list[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    post_id: str
    risk_level: str
    reasons: list[str]
    confidence: float

    @classmethod
    def from_domain(cls, result: AnalysisResult) -> Self:
        return cls(
            post_id=result.post_id,
            risk_level=result.risk_level.value,
            reasons=result.reasons,
            confidence=result.confidence,
        )
