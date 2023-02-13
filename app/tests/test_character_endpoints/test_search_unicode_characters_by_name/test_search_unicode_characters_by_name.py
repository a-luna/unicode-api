from fastapi.testclient import TestClient

from app.main import app
from app.tests.test_character_endpoints.test_search_unicode_characters_by_name.data import (
    SEARCH_TERM_HOME,
    SEARCH_TERM_HOUSE_PAGE_1_OF_2,
    SEARCH_TERM_HOUSE_PAGE_2_OF_2,
    SEARCH_TERM_HOUSE_PAGE_3_OF_2,
)

client = TestClient(app)


def test_search_term_home():
    response = client.get("/v1/characters/search?name=home")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_HOME


def test_search_term_house_page_1_of_3():
    response = client.get("/v1/characters/search?name=house")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_HOUSE_PAGE_1_OF_2


def test_search_term_house_page_2_of_3():
    response = client.get("/v1/characters/search?name=house&page=2")
    assert response.status_code == 200
    assert response.json() == SEARCH_TERM_HOUSE_PAGE_2_OF_2


def test_search_term_house_page_3_of_3():
    response = client.get("/v1/characters/search?name=house&page=3")
    assert response.status_code == 400
    assert response.json() == SEARCH_TERM_HOUSE_PAGE_3_OF_2
