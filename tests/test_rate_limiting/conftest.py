import os

import pytest
from fastapi.testclient import TestClient

from unicode_api.constants import ENV_TEST

os.environ["ENV"] = ENV_TEST


@pytest.fixture(scope="function")
def client():
    from unicode_api.main import app

    with TestClient(app) as client:
        client.headers = {"x-verify-rate-limiting": "true"}
        yield client
