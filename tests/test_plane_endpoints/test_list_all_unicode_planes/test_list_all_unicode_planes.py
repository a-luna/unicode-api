from fastapi import status

from tests.test_plane_endpoints.test_list_all_unicode_planes.data import ALL_PLANES, INVALID_PLANE_ID, UNASSIGNED_PLANE


def test_get_all_planes(client):
    response = client.get("/v1/planes")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == ALL_PLANES


def test_get_unassigned_plane(client):
    response = client.get("/v1/planes/10")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == UNASSIGNED_PLANE


def test_get_invalid_plane_id(client):
    response = client.get("/v1/planes/189")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == INVALID_PLANE_ID
