from app.tests.test_block_endpoints.test_list_all_unicode_blocks.data import (
    ALL_BLOCKS_ENDING_BEFORE_171_LIMIT_15,
    BOTH_START_AFTER_END_BEFORE_INVALID,
    INALID_PLANE_ABBREVIATION,
    PLANE_BMP_START_AFTER_57_LIMIT_20,
    PLANE_TIP_START_AFTER_20_LIMIT_15,
)


def test_get_all_blocks_in_bmp_start_after_57_limit_20(client):
    response = client.get("/v1/blocks?limit=20&starting_after=57&plane=BMP")
    assert response.status_code == 200
    assert response.json() == PLANE_BMP_START_AFTER_57_LIMIT_20


def test_get_all_blocks_end_before_171_limit_15(client):
    response = client.get("/v1/blocks?limit=15&ending_before=171")
    assert response.status_code == 200
    assert response.json() == ALL_BLOCKS_ENDING_BEFORE_171_LIMIT_15


def test_plane_tip_start_after_invalid(client):
    response = client.get("/v1/blocks?limit=15&starting_after=20&plane=TIP")
    assert response.status_code == 400
    assert response.json() == PLANE_TIP_START_AFTER_20_LIMIT_15


def test_both_start_after_end_before_invalid(client):
    response = client.get("/v1/blocks?starting_after=10&ending_before=33")
    assert response.status_code == 400
    assert response.json() == BOTH_START_AFTER_END_BEFORE_INVALID


def test_invalid_plane_abbreviation(client):
    response = client.get("/v1/blocks?plane=BDP")
    assert response.status_code == 400
    assert response.json() == INALID_PLANE_ABBREVIATION
