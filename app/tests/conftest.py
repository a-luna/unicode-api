import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client(request):
    from app.main import app

    with TestClient(app) as client:
        headers = {}
        headers[os.environ.get("TEST_HEADER", "").lower()] = "true"
        client.headers = headers
        yield client


@pytest.fixture(scope="function", autouse=True)
def set_env(request):
    os.environ["ENV"] = "TEST"
