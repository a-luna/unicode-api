from tests.test_rate_limiting.data import ALL_PLANES, PLANE_0


def test_rate_limiting(client):
    response = client.get("/v1/planes")
    assert response.status_code == 200
    assert response.json() == ALL_PLANES
    response = client.get("/v1/planes/0")
    assert response.status_code == 200
    assert response.json() == PLANE_0
    response = client.get("/v1/planes/1")
    assert response.status_code == 429
    assert "API rate limit of 2 requests in 1.0 second exceeded" in response.json()
