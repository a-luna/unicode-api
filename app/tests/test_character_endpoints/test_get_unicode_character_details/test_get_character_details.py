import pytest
from fastapi.testclient import TestClient
from humps import camelize

import app.schemas.enums as enum
from app.data.encoding import get_uri_encoded_value
from app.db.character_props import CHARACTER_PROPERTY_GROUPS
from app.main import app
from app.tests.test_character_endpoints.test_get_unicode_character_details.data import (
    ALL_CHARACTER_PROPERTIES,
    ALL_PROP_GROUP_NAMES,
    INVALID_PROP_GROUP_NAMES,
)

client = TestClient(app)


def get_character_properties(char, prop_group):
    prop_data = ALL_CHARACTER_PROPERTIES[char]
    char_props = {}
    if prop_group == enum.CharPropertyGroup.All:
        for group in enum.CharPropertyGroup:
            if group not in [enum.CharPropertyGroup.All, enum.CharPropertyGroup.NONE]:
                char_props.update(get_prop_group(group, prop_data))
    else:
        char_props = get_prop_group(prop_group, prop_data)
        char_props.update(get_prop_group(enum.CharPropertyGroup.Minimum, prop_data))
    return char_props


def get_prop_group(prop_group, prop_data):
    return {
        camelize(prop_details["name_out"]): prop_data[camelize(prop_details["name_out"])]
        for prop_details in CHARACTER_PROPERTY_GROUPS[prop_group]
        if camelize(prop_details["name_out"]) in prop_data
    }


@pytest.mark.parametrize("char", ALL_CHARACTER_PROPERTIES.keys())
def test_get_character_details_default(char):
    url = f"/v1/characters/{char}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/{get_uri_encoded_value(char)}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, enum.CharPropertyGroup.Minimum)]


@pytest.mark.parametrize("char", ALL_CHARACTER_PROPERTIES.keys())
@pytest.mark.parametrize("prop_group", ALL_PROP_GROUP_NAMES)
def test_get_character_details_show_props(char, prop_group):
    url = f"/v1/characters/{char}?show_props={prop_group}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/{get_uri_encoded_value(char)}?show_props={prop_group}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, enum.CharPropertyGroup.match_loosely(prop_group))]


def test_invalid_prop_group_name():
    response = client.get("/v1/characters/%F0%9B%B1%A0?show_props=foo&show_props=bar&show_props=baz")
    assert response.status_code == 400
    assert response.json() == INVALID_PROP_GROUP_NAMES
