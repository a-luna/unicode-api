import operator
from functools import reduce

import pytest

from app.core.cache import cached_data
from app.core.encoding import get_uri_encoded_value
from app.db.character_props import PROPERTY_GROUPS
from app.db.procs.get_char_details import get_prop_groups
from app.schemas.enums import CharPropertyGroup
from app.schemas.util import to_lower_camel
from app.tests.test_character_endpoints.test_get_unicode_character_details.data import (
    ALL_PROP_GROUP_NAMES,
    CHARACTER_PROPERTIES,
    INVALID_PROP_GROUP_NAMES,
    VERBOSE_CHARACTER_PROPERTIES,
)


def get_character_properties(char, prop_group, verbose=False):
    prop_groups = get_prop_groups(ord(char), [prop_group])
    char_prop_dicts = [get_prop_group(char, group, verbose) for group in prop_groups]
    return reduce(operator.ior, char_prop_dicts, {})


def get_prop_group(char, prop_group, verbose):
    prop_data = CHARACTER_PROPERTIES[char] if not verbose else VERBOSE_CHARACTER_PROPERTIES[char]
    return {
        to_lower_camel(prop_details["name_out"]): prop_data[to_lower_camel(prop_details["name_out"])]
        for prop_details in PROPERTY_GROUPS[prop_group]
        if to_lower_camel(prop_details["name_out"]) in prop_data
    }


@pytest.mark.parametrize("char", CHARACTER_PROPERTIES.keys())
def test_get_character_details_default(char, client):
    url = f"/v1/characters/-/{char}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/-/{get_uri_encoded_value(char)}"
    prop_group = (
        CharPropertyGroup.MINIMUM if not cached_data.character_is_unihan(ord(char)) else CharPropertyGroup.CJK_MINIMUM
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, prop_group, False)]


@pytest.mark.parametrize("q_verbose, verbose", [("&verbose=true", True), ("&verbose=false", False), ("", None)])
@pytest.mark.parametrize("char", CHARACTER_PROPERTIES.keys())
@pytest.mark.parametrize("prop_group", ALL_PROP_GROUP_NAMES)
def test_get_character_details_show_props(q_verbose, verbose, char, prop_group, client):
    url = f"/v1/characters/-/{char}?show_props={prop_group}{q_verbose}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/-/{get_uri_encoded_value(char)}?show_props={prop_group}{q_verbose}"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, CharPropertyGroup.match_loosely(prop_group), verbose)]


def test_invalid_prop_group_name(client):
    response = client.get("/v1/characters/-/%F0%9B%B1%A0?show_props=foo&show_props=bar&show_props=baz")
    assert response.status_code == 400
    assert response.json() == INVALID_PROP_GROUP_NAMES
