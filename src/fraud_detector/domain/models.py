from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
