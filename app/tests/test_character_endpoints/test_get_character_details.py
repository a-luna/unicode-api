import pytest
from fastapi.testclient import TestClient
from humps import camelize

from app.db.character_props import CHARACTER_PROPERTY_GROUPS
from app.main import app
from app.schemas.enums.property_group import CharPropertyGroup
from app.tests.test_character_endpoints.data import ALL_CHARACTER_PROPERTIES

client = TestClient(app)


def get_character_properties(char, prop_group):
    prop_data = ALL_CHARACTER_PROPERTIES[char]
    minimum = get_prop_group(CharPropertyGroup.Minimum, prop_data)
    char_props = {}
    if prop_group == CharPropertyGroup.All:
        for group in CharPropertyGroup:
            if group != CharPropertyGroup.All:
                char_props.update(get_prop_group(group, prop_data))
    else:
        char_props = get_prop_group(prop_group, prop_data)
    return char_props | minimum


def get_prop_group(prop_group, prop_data):
    return {
        camelize(prop_details["name_out"]): prop_data[camelize(prop_details["name_out"])]
        for prop_details in CHARACTER_PROPERTY_GROUPS[prop_group]
    }


@pytest.mark.parametrize("char", ALL_CHARACTER_PROPERTIES.keys())
def test_get_character_details_default(char):
    response = client.get(f"/v1/characters/{char}")
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, CharPropertyGroup.Minimum)]


@pytest.mark.parametrize("char", ALL_CHARACTER_PROPERTIES.keys())
@pytest.mark.parametrize(
    "prop_group",
    [prop_group for prop_group in CharPropertyGroup],
)
def test_get_character_details_show_props(char, prop_group):
    response = client.get(f"/v1/characters/{char}?show_props={prop_group.name}")
    assert response.status_code == 200
    assert response.json() == [get_character_properties(char, prop_group)]
