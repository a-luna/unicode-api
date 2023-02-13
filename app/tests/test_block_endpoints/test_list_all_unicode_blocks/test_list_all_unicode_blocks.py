from fastapi.testclient import TestClient

from app.main import app
from app.tests.test_block_endpoints.test_list_all_unicode_blocks.data import (
    ALL_BLOCKS_ENDING_BEFORE_171_LIMIT_15,
    BLOCKS_IN_BMP_START_AFTER_57_LIMIT_20,
    PLANE_TIP_START_AFTER_20_LIMIT_15,
)

client = TestClient(app)


def test_get_all_blocks_in_bmp_start_after_57_limit_20():
    response = client.get("/v1/blocks?limit=20&starting_after=57&plane=BASIC_MULTILINGUAL_PLANE")
    assert response.status_code == 200
    assert response.json() == BLOCKS_IN_BMP_START_AFTER_57_LIMIT_20


def test_get_all_blocks_end_before_171_limit_15():
    response = client.get("/v1/blocks?limit=15&ending_before=171")
    assert response.status_code == 200
    assert response.json() == ALL_BLOCKS_ENDING_BEFORE_171_LIMIT_15


def test_plane_tip_start_after_invalid():
    response = client.get("/v1/blocks?limit=15&starting_after=20&plane=TERTIARY_IDEOGRAPHIC_PLANE")
    assert response.status_code == 400
    assert response.json() == PLANE_TIP_START_AFTER_20_LIMIT_15
