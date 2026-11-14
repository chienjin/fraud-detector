from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from fraud_detector.api.main import app, get_analyzer
from fraud_detector.domain.errors import AnalysisFailedError, ExternalServiceUnavailableError
from fraud_detector.domain.models import AnalysisResult, Post, RiskLevel
from fraud_detector.services.analysis import TextAnalyzer


class StubAnalyzer:
    def analyze(self, post: Post) -> AnalysisResult:
        return AnalysisResult(
            post_id=post.id, risk_level=RiskLevel.HIGH, reasons=["stub"], confidence=0.9
        )


class UnavailableAnalyzer:
    def analyze(self, post: Post) -> AnalysisResult:
        raise ExternalServiceUnavailableError("down")


class BrokenAnalyzer:
    def analyze(self, post: Post) -> AnalysisResult:
        raise AnalysisFailedError("down")


@pytest.fixture(autouse=True)
def clear_overrides() -> Iterator[None]:
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides[get_analyzer] = StubAnalyzer
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_analysis_returns_result_from_analyzer(client: TestClient) -> None:
    response = client.post("/analyses", json={"text": "保證獲利，快加LINE"})

    assert response.status_code == 201
    body = response.json()
    assert body["risk_level"] == "high"
    assert body["reasons"] == ["stub"]


def test_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/analyses", json={"text": ""})

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("analyzer", "status_code", "detail"),
    [
        (UnavailableAnalyzer, 503, "分析服務暫時無法使用，請稍後再試"),
        (BrokenAnalyzer, 502, "分析服務出現錯誤，請稍後再試"),
    ],
)
def test_analyzer_errors_are_translated_to_http_status(
    analyzer: type[TextAnalyzer], status_code: int, detail: str
) -> None:
    app.dependency_overrides[get_analyzer] = analyzer

    response = TestClient(app).post("/analyses", json={"text": "保證獲利"})

    assert response.status_code == status_code
    assert response.json() == {"detail": detail}
