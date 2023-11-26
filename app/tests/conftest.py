import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def client(request):
    os.environ["ENV"] = "TEST"
    from app.main import app

    with TestClient(app) as client:
        headers = {}
        headers[os.environ.get("TEST_HEADER", "").lower()] = "true"
        client.headers = headers
        yield client
