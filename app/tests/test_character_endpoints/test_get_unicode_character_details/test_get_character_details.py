import operator
from functools import reduce

import pytest
from fastapi.testclient import TestClient
from humps import camelize

from app.data.cache import cached_data
from app.data.encoding import get_uri_encoded_value
from app.db.character_props import PROPERTY_GROUPS
from app.db.get_char_details import get_prop_groups
from app.main import app
from app.schemas.enums import CharPropertyGroup
from app.tests.test_character_endpoints.test_get_unicode_character_details.data import (
    ALL_CHARACTER_PROPERTIES,
    ALL_PROP_GROUP_NAMES,
    INVALID_PROP_GROUP_NAMES,
)

client = TestClient(app)


def get_character_properties(char, prop_group):
    prop_data = ALL_CHARACTER_PROPERTIES[char]
    prop_groups = get_prop_groups(ord(char), [prop_group])
    char_prop_dicts = [get_prop_group(group, prop_data) for group in prop_groups]
    return reduce(operator.ior, char_prop_dicts, {})


def get_prop_group(prop_group, prop_data):
    return {
        camelize(prop_details["name_out"]): prop_data[camelize(prop_details["name_out"])]
        for prop_details in PROPERTY_GROUPS[prop_group]
        if camelize(prop_details["name_out"]) in prop_data
    }


@pytest.mark.parametrize("char", ALL_CHARACTER_PROPERTIES.keys())
def test_get_character_details_default(char):
    url = f"/v1/characters/{char}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/{get_uri_encoded_value(char)}"
    prop_group = (
        CharPropertyGroup.MINIMUM if not cached_data.character_is_unihan(ord(char)) else CharPropertyGroup.CJK_MINIMUM
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, prop_group)]


@pytest.mark.parametrize("char", ALL_CHARACTER_PROPERTIES.keys())
@pytest.mark.parametrize("prop_group", ALL_PROP_GROUP_NAMES)
def test_get_character_details_show_props(char, prop_group):
    url = f"/v1/characters/{char}?show_props={prop_group}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/{get_uri_encoded_value(char)}?show_props={prop_group}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, CharPropertyGroup.match_loosely(prop_group))]


def test_invalid_prop_group_name():
    response = client.get("/v1/characters/%F0%9B%B1%A0?show_props=foo&show_props=bar&show_props=baz")
    assert response.status_code == 400
    assert response.json() == INVALID_PROP_GROUP_NAMES
