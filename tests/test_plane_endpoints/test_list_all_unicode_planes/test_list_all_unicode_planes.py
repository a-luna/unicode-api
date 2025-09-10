from tests.test_plane_endpoints.test_list_all_unicode_planes.data import ALL_PLANES, UNASSIGNED_PLANE


def test_get_all_planes(client):
    response = client.get("/v1/planes")
    assert response.status_code == 200
    assert response.json() == ALL_PLANES


def test_get_unassigned_plane(client):
    response = client.get("/v1/planes/10")
    assert response.json() == UNASSIGNED_PLANE
