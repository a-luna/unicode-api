from fastapi.testclient import TestClient

from app.main import app
from app.tests.test_character_endpoints.test_list_all_unicode_characters.data import (
    ALL_CHARS_START_AFTER_172E_LIMIT_25,
    BLOCK_COUNTING_ROD_NUMERALS_END_BEFORE_1D380,
    BLOCK_MIAO_START_AFTER_DEF_LIMIT_DEF,
    BLOCK_THAI_START_AFTER_INVALID,
    BOTH_START_AFTER_END_BEFORE_INVALID,
    INVALID_BLOCK_NAME,
    INVALID_BLOCK_NAME_NO_FUZZY_MATCHES,
    INVALID_CODEPOINT_STRING_1,
    INVALID_CODEPOINT_STRING_2,
)

client = TestClient(app)


def test_get_all_chars_start_after_172E_limit_25():
    response = client.get("/v1/characters?limit=25&starting_after=172E")
    assert response.status_code == 200
    assert response.json() == ALL_CHARS_START_AFTER_172E_LIMIT_25


def test_block_miao_start_after_def_limit_def():
    response = client.get("/v1/characters?block=MIAO")
    assert response.status_code == 200
    assert response.json() == BLOCK_MIAO_START_AFTER_DEF_LIMIT_DEF


def test_counting_rod_numerals_end_before_1d380():
    response = client.get("/v1/characters?ending_before=1D380&block=COUNTING_ROD_NUMERALS")
    assert response.status_code == 200
    assert response.json() == BLOCK_COUNTING_ROD_NUMERALS_END_BEFORE_1D380


def test_block_thai_start_after_invalid():
    response = client.get("/v1/characters?starting_after=16F00&block=THAI")
    assert response.status_code == 400
    assert response.json() == BLOCK_THAI_START_AFTER_INVALID


def test_both_start_after_end_before_invalid():
    response = client.get("/v1/characters?starting_after=23ff&ending_before=240f")
    assert response.status_code == 400
    assert response.json() == BOTH_START_AFTER_END_BEFORE_INVALID


def test_invalid_codepoint_string_1():
    response = client.get("/v1/characters?starting_after=U%2B49")
    assert response.status_code == 400
    assert response.json() == INVALID_CODEPOINT_STRING_1


def test_invalid_codepoint_string_2():
    response = client.get("/v1/characters?starting_after=U%2B110000")
    assert response.status_code == 400
    assert response.json() == INVALID_CODEPOINT_STRING_2


def test_invalid_block_name():
    response = client.get("/v1/characters?block=ancient%20numbers")
    assert response.status_code == 400
    assert response.json() == INVALID_BLOCK_NAME


def test_invalid_block_name_no_fuzzy_matches():
    response = client.get("/v1/characters?block=blah")
    assert response.status_code == 400
    assert response.json() == INVALID_BLOCK_NAME_NO_FUZZY_MATCHES
