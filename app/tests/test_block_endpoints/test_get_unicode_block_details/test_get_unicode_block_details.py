from fastapi.testclient import TestClient

from app.main import app
from app.tests.test_block_endpoints.test_get_unicode_block_details.data import BLOCK_HEBREW

client = TestClient(app)


def test_get_block_hebrew():
    response = client.get("v1/blocks/HEBREW")
    assert response.status_code == 200
    assert response.json() == BLOCK_HEBREW
