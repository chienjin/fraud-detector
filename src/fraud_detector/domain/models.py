from dataclasses import dataclass
from datetime import datetime
from enum import Enum

MIN_CONFIDENCE = 0
MAX_CONFIDENCE = 1


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Post:
    id: str
    text: str
    image_urls: list[str]
    created_at: datetime


@dataclass(frozen=True)
class AnalysisResult:
    post_id: str
    risk_level: RiskLevel
    reasons: list[str]
    confidence: float

    def __post_init__(self) -> None:
        if self.confidence < MIN_CONFIDENCE or self.confidence > MAX_CONFIDENCE:
            raise ValueError(
                f"confidence must be between {MIN_CONFIDENCE} and {MAX_CONFIDENCE},got {self.confidence}"
            )
