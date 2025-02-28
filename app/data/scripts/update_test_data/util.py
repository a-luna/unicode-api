from typing import Any

from app.models.util import to_lower_camel


def pythonize_that_json(json_str: str) -> str:
    return json_str.replace("null", "None").replace("false", "False").replace("true", "True")


def format_response_property_names(response: dict[str, Any]) -> dict[str, Any]:
    formatted = {}
    for prop_name, prop_value in response.items():
        if isinstance(prop_value, dict):
            formatted[to_lower_camel(prop_name)] = format_response_property_names(prop_value)
        if isinstance(prop_value, list):
            formatted_list = []
            for item in prop_value:
                if isinstance(item, dict):
                    formatted_list.append(format_response_property_names(item))
                else:
                    formatted_list.append(item)
            formatted[to_lower_camel(prop_name)] = formatted_list
        else:
            formatted[to_lower_camel(prop_name)] = prop_value
    return formatted
