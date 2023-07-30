import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client(request):
    with TestClient(app) as client:
        headers = {}
        headers[os.environ.get("TEST_HEADER", "").lower()] = "true"
        client.headers = headers
        yield client
