from fastapi.testclient import TestClient

from app.main import app
from app.tests.test_character_endpoints.test_filter_unicode_characters.data import (
    FILTER_BY_UNICODE_AGE,
    INVALID_PAGE_NUMBER,
    NAME_SPIRITUS_CATEGORY_MN_SCRIPT_COPT,
    NO_CHARS_MATCH_SETTINGS,
)

client = TestClient(app)


def test_filter_name_spiritus_category_mn_script_copt():
    response = client.get("/v1/characters/filter?name=spiritus&category=mn&script=copt")
    assert response.status_code == 200
    assert response.json() == NAME_SPIRITUS_CATEGORY_MN_SCRIPT_COPT


def test_invalid_page_number():
    response = client.get("/v1/characters/filter?name=spiritus&category=mn&script=copt&page=2")
    assert response.status_code == 400
    assert response.json() == INVALID_PAGE_NUMBER


def test_no_characters_match_filter_settings():
    response = client.get("/v1/characters/filter?name=test&script=copt&per_page=100&page=1")
    assert response.status_code == 200
    assert response.json() == NO_CHARS_MATCH_SETTINGS


def test_filter_by_unicode_age():
    response = client.get("/v1/characters/filter?category=sk&age=13.0&age=14.0&age=15.0")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_UNICODE_AGE
