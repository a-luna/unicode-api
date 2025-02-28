import operator
from functools import reduce
from typing import Any

import pytest

import app.db.models as db
from app.core.cache import cached_data
from app.core.encoding import get_uri_encoded_value
from app.db.character_props import PROPERTY_GROUPS
from app.db.procs.get_char_details import get_prop_groups
from app.models.util import to_lower_camel
from app.tests.test_character_endpoints.test_get_unicode_character_details.data import (
    CHARACTER_PROPERTIES,
    INVALID_PROP_GROUP_NAMES,
    VERBOSE_CHARACTER_PROPERTIES,
)


def get_all_prop_group_names() -> list[str]:
    prop_names = [
        prop_group.normalized for prop_group in db.CharPropertyGroup if prop_group != db.CharPropertyGroup.NONE
    ]
    prop_aliases = [prop_group.short_alias for prop_group in db.CharPropertyGroup if prop_group.has_alias]
    return list(set(prop_names + prop_aliases))


def get_character_properties(char: str, prop_group: db.CharPropertyGroup, verbose: bool = False) -> dict[str, Any]:
    prop_groups = get_prop_groups(ord(char), [prop_group])
    char_prop_dicts = [get_prop_group_values_for_char(char, group, verbose) for group in prop_groups]
    return reduce(operator.ior, char_prop_dicts, {})


def get_prop_group_values_for_char(
    char: str, prop_group: db.CharPropertyGroup, verbose: bool = False
) -> dict[str, Any]:
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
        db.CharPropertyGroup.MINIMUM
        if not cached_data.character_is_unihan(ord(char))
        else db.CharPropertyGroup.CJK_MINIMUM
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, prop_group, False)]


@pytest.mark.parametrize("q_verbose, verbose", [("&verbose=true", True), ("&verbose=false", False), ("", None)])
@pytest.mark.parametrize("char", CHARACTER_PROPERTIES.keys())
@pytest.mark.parametrize("group_name", get_all_prop_group_names())
def test_get_character_details_show_props(q_verbose, verbose, char, group_name, client):
    url = f"/v1/characters/-/{char}?show_props={group_name}{q_verbose}"
    if any(char.isascii() and not char.isprintable() for char in url):
        url = f"/v1/characters/-/{get_uri_encoded_value(char)}?show_props={group_name}{q_verbose}"
    response = client.get(url)
    assert response.status_code == 200

    prop_group = db.CharPropertyGroup.match_loosely(group_name)
    assert prop_group is not None
    assert response.json() == [get_character_properties(char, prop_group, verbose)]


def test_invalid_prop_group_name(client):
    response = client.get("/v1/characters/-/%F0%9B%B1%A0?show_props=foo&show_props=bar&show_props=baz")
    assert response.status_code == 400
    assert response.json() == INVALID_PROP_GROUP_NAMES
