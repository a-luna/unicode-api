from app.tests.test_block_endpoints.test_get_unicode_block_details.data import (
    BLOCK_ETHIOPIC_EXTENDED_A,
    BLOCK_GREEK_SHORTNAME,
    BLOCK_HEBREW,
    INVALID_BLOCK_NAME,
)


def test_get_block_hebrew(client):
    response = client.get("v1/blocks/HEBREW")
    assert response.status_code == 200
    assert response.json() == BLOCK_HEBREW


def test_get_ethiopic_extended_a(client):
    response = client.get("v1/blocks/ETHIOPIC_EXTENDED_A")
    assert response.status_code == 200
    assert response.json() == BLOCK_ETHIOPIC_EXTENDED_A


def test_get_block_from_shortname(client):
    response = client.get("/v1/blocks/greek")
    assert response.status_code == 200
    assert response.json() == BLOCK_GREEK_SHORTNAME


def test_invalid_block_name(client):
    response = client.get("/v1/blocks/smoke%20signals")
    assert response.status_code == 400
    assert response.json() == INVALID_BLOCK_NAME
