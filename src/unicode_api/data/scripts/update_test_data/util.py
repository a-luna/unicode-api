def convert_json_to_python_literals(json_str: str) -> str:
    """
    Converts a JSON-formatted string to a Python-compatible string by replacing JSON literals
    ('null', 'false', 'true') with their Python equivalents ('None', 'False', 'True').

    Args:
        json_str (str): The JSON-formatted string to convert.

    Returns:
        str: The input string with JSON literals replaced by Python equivalents.
    """
    return json_str.replace("null", "None").replace("false", "False").replace("true", "True")
