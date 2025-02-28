from app.tests.test_block_endpoints.test_search_unicode_blocks_by_name.data import (
    SEARCH_TERM_BLAH,
    SEARCH_TERM_CAP,
    SEARCH_TERM_OLD_PER_PAGE_5_PAGE_1_OF_2,
    SEARCH_TERM_OLD_PER_PAGE_5_PAGE_2_OF_2,
    SEARCH_TERM_OLD_PER_PAGE_5_PAGE_3_OF_2,
)


def test_search_term_cap(client):
    response = client.get("/v1/blocks/search?name=cap")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_CAP


def test_search_term_old_page_1_of_2(client):
    response = client.get("/v1/blocks/search?name=old&per_page=5")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_OLD_PER_PAGE_5_PAGE_1_OF_2


def test_search_term_old_page_2_of_2(client):
    response = client.get("/v1/blocks/search?name=old&per_page=5&page=2")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_OLD_PER_PAGE_5_PAGE_2_OF_2


def test_search_term_old_page_3_of_2(client):
    response = client.get("/v1/blocks/search?name=old&per_page=5&page=3")
    assert response.status_code == 400
    assert response.json() == SEARCH_TERM_OLD_PER_PAGE_5_PAGE_3_OF_2


def test_search_term_blah(client):
    response = client.get("/v1/blocks/search?name=blah")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_BLAH
