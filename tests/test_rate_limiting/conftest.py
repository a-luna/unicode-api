import os

import pytest
from fastapi.testclient import TestClient

os.environ["ENV"] = "TEST"


@pytest.fixture(scope="function")
def client():
    from unicode_api.main import app

    with TestClient(app) as client:
        client.headers = {"x-verify-rate-limiting": "true"}
        yield client
