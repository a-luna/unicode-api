from html.entities import html5

"""
This module provides utility functions for encoding and decoding Unicode characters
into various formats, including HTML entities, UTF-8, UTF-16, UTF-32, and URI encoding.

Functions:
    get_codepoint_string(codepoint: int) -> str:
        Converts a Unicode code point into its string representation in the format "U+XXXX".

    get_html_entities(codepoint: int) -> list[str]:
        Returns a list of HTML entity representations for a given Unicode code point,
        including numeric and named entities (if available).

    get_utf8_dec_bytes(uni_char: str) -> list[int]:
        Encodes a Unicode character into UTF-8 and returns the decimal byte values.

    get_utf8_hex_bytes(uni_char: str) -> list[str]:
        Encodes a Unicode character into UTF-8 and returns the hexadecimal byte values.

    get_utf8_value(uni_char: str) -> str:
        Encodes a Unicode character into UTF-8 and returns a space-separated string
        of hexadecimal byte values prefixed with "0x".

    get_uri_encoded_value(uni_char: str) -> str:
        Encodes a Unicode character into its URI-encoded representation.

    get_utf16_hex_bytes(uni_char: str) -> list[str]:
        Encodes a Unicode character into UTF-16 (big-endian) and returns the hexadecimal
        byte values as a list of strings.

    get_utf16_dec_bytes(uni_char: str) -> list[int]:
        Encodes a Unicode character into UTF-16 (big-endian) and returns the decimal
        byte values as a list of integers.

    get_utf16_value(uni_char: str) -> str:
        Encodes a Unicode character into UTF-16 (big-endian) and returns a space-separated
        string of hexadecimal byte values prefixed with "0x".

    get_utf32_hex_bytes(uni_char: str) -> list[str]:
        Encodes a Unicode character into UTF-32 and returns the hexadecimal byte value
        as a list containing a single string.

    get_utf32_dec_bytes(uni_char: str) -> list[int]:
        Encodes a Unicode character into UTF-32 and returns the decimal byte value
        as a list containing a single integer.

    get_utf32_value(uni_char: str) -> str:
        Encodes a Unicode character into UTF-32 and returns the hexadecimal byte value
        prefixed with "0x".
"""

HTML_ENTITY_MAP = dict(
    sorted([(ord(uni_char), entity) for (entity, uni_char) in html5.items() if len(uni_char) == 1], key=lambda x: x[0])
)


def get_codepoint_string(codepoint: int) -> str:
    """
    Convert a Unicode code point integer into its string representation in the format "U+XXXX".

    Args:
        codepoint (int): The Unicode code point to convert.

    Returns:
        str: The string representation of the code point in the format "U+XXXX", where "XXXX"
             is the uppercase hexadecimal value of the code point, zero-padded to at least four digits.
    """
    return f"U+{codepoint:04X}"


def get_html_entities(codepoint: int) -> list[str]:
    """
    Generate a list of HTML entities for a given Unicode code point.

    Args:
        codepoint (int): The Unicode code point to generate HTML entities for.

    Returns:
        list[str]: A list of HTML entities representing the code point. This
        includes the decimal numeric character reference (e.g., "&#123;"),
        the hexadecimal numeric character reference (e.g., "&#x7B;"), and,
        if available, the named character reference (e.g., "&lt;").
    """
    html_entities = [f"&#{codepoint};", f"&#x{codepoint:02X};"]
    named_entity = HTML_ENTITY_MAP.get(codepoint)
    return html_entities + [f"&{named_entity}"] if named_entity else html_entities


def get_utf8_dec_bytes(uni_char: str) -> list[int]:
    """
    Convert a single Unicode character to its UTF-8 encoded byte values in decimal format.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        list[int]: A list of integers representing the UTF-8 encoded byte values of the input character.

    Raises:
        AttributeError: If the input is not a string.
        TypeError: If the input string contains more than one character.
    """
    return list(uni_char.encode())


def get_utf8_hex_bytes(uni_char: str) -> list[str]:
    """
    Convert a Unicode character to its UTF-8 encoded hexadecimal byte representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        list[str]: A list of strings, where each string represents a hexadecimal byte
                   of the UTF-8 encoding of the input character, formatted as two
                   uppercase hexadecimal digits.
    """
    return [f"{x:02X}" for x in uni_char.encode()]


def get_utf8_value(uni_char: str) -> str:
    """
    Convert a Unicode character to its UTF-8 hexadecimal byte representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        str: A string containing the UTF-8 hexadecimal byte values of the input
        character, separated by spaces. Each byte is prefixed with "0x".

    Raises:
        ValueError: If the input is not a single Unicode character.
    """
    return " ".join(f"0x{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_uri_encoded_value(uni_char: str) -> str:
    """
    Convert a single Unicode character into its URI-encoded representation.

    This function takes a Unicode character, encodes it into UTF-8, and then
    converts each byte of the UTF-8 encoding into its percent-encoded form
    (e.g., '%20' for a space character).

    Args:
        uni_char (str): A single Unicode character to be URI-encoded.

    Returns:
        str: The URI-encoded representation of the input character.
    """
    return "".join(f"%{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_utf16_hex_bytes(uni_char: str) -> list[str]:
    """
    Convert a Unicode character to its UTF-16 hexadecimal byte representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        list[str]: A list of UTF-16 hexadecimal byte strings. For characters
                   represented by a single 16-bit code unit, the list contains
                   one string. For characters represented by a surrogate pair
                   (two 16-bit code units), the list contains two strings.
                   Returns an empty list if the input is invalid.
    """
    bytes_8bit = [f"{x:02X}" for x in uni_char.encode("utf_16_be")]
    return (
        [f"{bytes_8bit[0]}{bytes_8bit[1]}"]
        if len(bytes_8bit) == 2
        else [f"{bytes_8bit[0]}{bytes_8bit[1]}", f"{bytes_8bit[2]}{bytes_8bit[3]}"]
        if len(bytes_8bit) == 4
        else []
    )


def get_utf16_dec_bytes(uni_char: str) -> list[int]:
    """
    Convert a Unicode character into its UTF-16 representation as a list of decimal byte values.

    Args:
        uni_char (str): A single Unicode character to be converted.

    Returns:
        list[int]: A list of integers representing the UTF-16 encoded bytes of the input character in decimal format.

    Note:
        This function relies on an external function `get_utf16_hex_bytes` to obtain the UTF-16 encoded bytes in hexadecimal format.
    """
    return [int(byte, 16) for byte in get_utf16_hex_bytes(uni_char)]


def get_utf16_value(uni_char: str) -> str:
    """
    Convert a Unicode character to its UTF-16 hexadecimal representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        str: A string containing the UTF-16 hexadecimal values of the character,
             separated by spaces. Each value is prefixed with "0x".

    Raises:
        ValueError: If the input is not a single Unicode character.
    """
    return " ".join(f"0x{byte}" for byte in get_utf16_hex_bytes(uni_char))


def get_utf32_hex_bytes(uni_char: str) -> list[str]:
    """
    Convert a single Unicode character to its UTF-32 hexadecimal byte representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        list[str]: A list containing the UTF-32 hexadecimal byte representation
                   of the input character as an 8-character uppercase string.
    """
    return [f"{ord(uni_char):08X}"]


def get_utf32_dec_bytes(uni_char: str) -> list[int]:
    """
    Convert a Unicode character to its UTF-32 decimal byte representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        list[int]: A list containing the UTF-32 representation of the character as a decimal integer.
    """
    return [int(get_utf32_value(uni_char), 16)]


def get_utf32_value(uni_char: str) -> str:
    """
    Convert a single Unicode character to its UTF-32 hexadecimal representation.

    Args:
        uni_char (str): A single Unicode character.

    Returns:
        str: The UTF-32 hexadecimal representation of the input character,
             formatted as a string prefixed with "0x" and padded to 8 digits.

    Raises:
        TypeError: If the input is not a string or contains more than one character.
    """
    return f"0x{ord(uni_char):08X}"
