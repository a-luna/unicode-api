from app.tests.test_codepoint_endpoints.test_get_unicode_character_at_codepoint.data import (
    CODEPOINT_24AF_RAW_HEX,
    CODEPOINT_24AF_WITH_PREFIX_1,
    CODEPOINT_24AF_WITH_PREFIX_2,
    INVALID_HEX_DIGIT_1,
    INVALID_HEX_DIGIT_2,
    INVALID_LEADING_ZEROS,
    INVALID_OUT_OF_RANGE,
    INVALID_PROP_GROUP_NAME,
)


def test_get_character_at_codepoint_raw_hex(client):
    response = client.get("v1/codepoints/24AF")
    assert response.status_code == 200
    assert response.json() == CODEPOINT_24AF_RAW_HEX


def test_get_character_at_codepoint_with_prefix_1(client):
    response = client.get("v1/codepoints/U+24AF?show_props=basic&verbose=true")
    assert response.status_code == 200
    assert response.json() == CODEPOINT_24AF_WITH_PREFIX_1


def test_get_character_at_codepoint_with_prefix_2(client):
    response = client.get("v1/codepoints/0x24AF?show_props=all")
    assert response.status_code == 200
    assert response.json() == CODEPOINT_24AF_WITH_PREFIX_2


def test_get_character_at_codepoint_invalid_single_hex_digit(client):
    response = client.get("v1/codepoints/0x24AZ")
    assert response.status_code == 400
    assert response.json() == INVALID_HEX_DIGIT_1


def test_get_character_at_codepoint_invalid_multiple_hex_digits(client):
    response = client.get("v1/codepoints/maccaroni")
    assert response.status_code == 400
    assert response.json() == INVALID_HEX_DIGIT_2


def test_get_character_at_codepoint_invalid_leading_zeros(client):
    response = client.get("v1/codepoints/U+72")
    assert response.status_code == 400
    assert response.json() == INVALID_LEADING_ZEROS


def test_get_character_at_codepoint_invalid_out_of_range_1(client):
    response = client.get("v1/codepoints/U+1234567")
    assert response.status_code == 400
    assert response.json() == INVALID_OUT_OF_RANGE


def test_get_character_at_codepoint_invalid_out_of_range_2(client):
    response = client.get("v1/codepoints/0x1234567")
    assert response.status_code == 400
    assert response.json() == INVALID_OUT_OF_RANGE


def test_get_character_at_codepoint_invalid_out_of_range_3(client):
    response = client.get("v1/codepoints/1234567")
    assert response.status_code == 400
    assert response.json() == INVALID_OUT_OF_RANGE


def test_get_character_at_codepoint_invalid_prop_group(client):
    response = client.get("v1/codepoints/U+0072?show_props=max")
    assert response.status_code == 400
    assert response.json() == INVALID_PROP_GROUP_NAME
