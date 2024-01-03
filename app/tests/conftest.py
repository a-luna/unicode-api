import os

import pytest
from fastapi.testclient import TestClient

os.environ["ENV"] = "TEST"


@pytest.fixture(scope="function")
def client():
    from app.main import app

    with TestClient(app) as client:
        headers = {}
        headers["x-verify-rate-limiting"] = "false"
        client.headers = headers
        yield client


@pytest.fixture(scope="function", autouse=True)
def set_env(request):
    os.environ["ENV"] = "TEST"
