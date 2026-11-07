from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, status

from fraud_detector.adapters.keyword_analyzer import KeywordAnalyzer
from fraud_detector.api.schemas import AnalysisResponse, AnalyzePostRequest
from fraud_detector.domain.models import Post
from fraud_detector.services.analysis import run_analysis
from fraud_detector.services.ports import TextAnalyzer

app = FastAPI(title="Fraud Detector")


def get_analyzer() -> TextAnalyzer:
    return KeywordAnalyzer()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyses", status_code=status.HTTP_201_CREATED)
def create_analysis(
    request: AnalyzePostRequest,
    analyzer: Annotated[TextAnalyzer, Depends(get_analyzer)],
) -> AnalysisResponse:
    post = Post(
        id=str(uuid4()),
        text=request.text,
        image_urls=request.image_urls,
        created_at=datetime.now(UTC),
    )
    result = run_analysis(post, analyzer)
    return AnalysisResponse.from_domain(result)
