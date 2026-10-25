from datetime import UTC, datetime

import pytest

from fraud_detector.domain.models import Post


@pytest.fixture
def sample_post() -> Post:
    return Post("1", "a", ["a.jpg"], datetime(2026, 10, 25, tzinfo=UTC))
