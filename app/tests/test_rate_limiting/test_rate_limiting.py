import os

import pytest
from fastapi.testclient import TestClient

from app.tests.test_rate_limiting.data import PLANE_0


@pytest.fixture
def client():
    os.environ["ENV"] = "TEST"
    from app.main import app

    with TestClient(app) as client:
        headers = {}
        headers["x-verify-rate-limiting"] = "true"
        client.headers = headers
        yield client


def test_rate_limiting(client):
    response = client.get("/v1/planes/0")
    assert response.status_code == 200
    assert response.json() == PLANE_0
    response = client.get("/v1/planes/0")
    assert response.status_code == 200
    assert response.json() == PLANE_0
    response = client.get("/v1/planes/0")
    assert response.status_code == 429
    response_json = response.json()
    assert "API rate limit of 2 requests in 1.0 second exceeded" in response_json
