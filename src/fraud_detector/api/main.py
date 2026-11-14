import logging
from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from fraud_detector.adapters.keyword_analyzer import KeywordAnalyzer
from fraud_detector.api.schemas import AnalysisResponse, AnalyzePostRequest
from fraud_detector.domain.errors import AnalysisFailedError, ExternalServiceUnavailableError
from fraud_detector.domain.models import Post
from fraud_detector.services.analysis import run_analysis
from fraud_detector.services.ports import TextAnalyzer

app = FastAPI(title="Fraud Detector")

logger = logging.getLogger(__name__)


@app.exception_handler(ExternalServiceUnavailableError)
def handle_service_unavailable(
    request: Request, exc: ExternalServiceUnavailableError
) -> JSONResponse:
    logger.warning("外部分析服務無法使用：%s", exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "分析服務暫時無法使用，請稍後再試"},
    )


@app.exception_handler(AnalysisFailedError)
def handle_analysis_failed(request: Request, exc: AnalysisFailedError) -> JSONResponse:
    logger.warning("外部分析服務結果結構錯誤: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": "分析服務出現錯誤，請稍後再試"},
    )


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
