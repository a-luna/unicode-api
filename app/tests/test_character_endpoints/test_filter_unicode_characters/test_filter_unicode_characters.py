from app.tests.test_character_endpoints.test_filter_unicode_characters.data import (
    FILTER_BY_BIDIRECTIONAL_CLASS,
    FILTER_BY_BLOCK_NAME,
    FILTER_BY_CCC,
    FILTER_BY_CHAR_FLAG,
    FILTER_BY_DECOMPOSITION_TYPE,
    FILTER_BY_JOINING_TYPE,
    FILTER_BY_LINE_BREAK_TYPE,
    FILTER_BY_NAME_BY_CATEGORY_BY_SCRIPT,
    FILTER_BY_NUMERIC_TYPE,
    FILTER_BY_UNICODE_AGE,
    INVALID_FILTER_PARAM_VALUES,
    INVALID_PAGE_NUMBER,
    NO_CHARS_MATCH_SETTINGS,
)


def test_filter_by_name_by_category_by_script(client):
    response = client.get("/v1/characters/filter?name=spiritus&category=mn&script=copt")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_NAME_BY_CATEGORY_BY_SCRIPT


def test_filter_by_unicode_age(client):
    response = client.get("/v1/characters/filter?category=sk&age=13.0&age=14.0&age=15.0")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_UNICODE_AGE


def test_filter_by_bidirectional_class(client):
    response = client.get("/v1/characters/filter?name=dong&bidi_class=et")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_BIDIRECTIONAL_CLASS


def test_filter_by_decomposition_type(client):
    response = client.get("/v1/characters/filter?name=seven&decomp_type=enc")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_DECOMPOSITION_TYPE


def test_filter_by_line_break_type(client):
    response = client.get("/v1/characters/filter?line_break=is")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_LINE_BREAK_TYPE


def test_filter_by_combining_class_category(client):
    response = client.get("/v1/characters/filter?ccc=214")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_CCC


def test_filter_by_numeric_type(client):
    response = client.get("/v1/characters/filter?script=khar&num_type=di")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_NUMERIC_TYPE


def test_filter_by_joining_type(client):
    response = client.get("/v1/characters/filter?join_type=l")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_JOINING_TYPE


def test_filter_by_char_flags(client):
    response = client.get("/v1/characters/filter?flag=Is%20Hyphen&per_page=20")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_CHAR_FLAG


def test_filter_by_block_name(client):
    response = client.get("/v1/characters/filter?block=Ancient_Symbols")
    assert response.status_code == 200
    assert response.json() == FILTER_BY_BLOCK_NAME


def test_no_characters_match_filter_settings(client):
    response = client.get("/v1/characters/filter?name=test&script=copt&show_props=all")
    assert response.status_code == 200
    assert response.json() == NO_CHARS_MATCH_SETTINGS


def test_invalid_page_number(client):
    response = client.get("/v1/characters/filter?name=spiritus&category=mn&script=copt&page=2")
    assert response.status_code == 400
    assert response.json() == INVALID_PAGE_NUMBER


def test_invalid_filter_param_values(client):
    response = client.get(
        "/v1/characters/filter"
        "?category=aa&category=bb"
        "&age=7.1&age=12.97"
        "&script=blar&script=blee"
        "&bidi_class=vv&bidi_class=rr"
        "&show_props=soup&show_props=salad"
        "&decomp_type=gosh"
        "&line_break=ha"
        "&ccc=300"
        "&num_type=dd"
        "&join_type=j"
        "&flag=special&flag=basic"
        "&block=xxx"
    )
    assert response.status_code == 400
    assert response.json() == INVALID_FILTER_PARAM_VALUES
