from app.tests.test_rate_limiting.data import PLANE_0


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
