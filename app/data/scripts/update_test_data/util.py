from typing import Any

from app.schemas.util import to_lower_camel


def pythonize_that_json(json: str) -> str:
    return json.replace("null", "None").replace("false", "False").replace("true", "True")


def convert_prop_names_to_camel(data: dict[str, Any]) -> dict[str, Any]:
    converted = {}
    for prop_name, prop_value in data.items():
        if isinstance(prop_value, dict):
            converted[to_lower_camel(prop_name)] = convert_prop_names_to_camel(prop_value)
        if isinstance(prop_value, list):
            converted[to_lower_camel(prop_name)] = [convert_prop_names_to_camel(item) for item in prop_value]
        else:
            converted[to_lower_camel(prop_name)] = prop_value
    return converted
