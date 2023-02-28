from fastapi.testclient import TestClient

from app.main import app
from app.tests.test_plane_endpoints.test_get_unicode_plane_details.data import PLANE_SMP

client = TestClient(app)


def test_get_plane_smp():
    response = client.get("v1/planes/1")
    assert response.status_code == 200
    assert response.json() == PLANE_SMP
