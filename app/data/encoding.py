from html.entities import html5

HTML_ENTITY_MAP = {
    cp: entity
    for (cp, entity) in sorted(
        [(ord(uni_char), entity) for (entity, uni_char) in html5.items() if len(uni_char) == 1],
        key=lambda x: x[0],
    )
}


def get_codepoint_string(codepoint: int) -> str:
    return f"U+{codepoint:04X}"


def get_html_entities(codepoint: int) -> list[str]:
    html_entities = [f"&#{codepoint};", f"&#x{codepoint:02X};"]
    named_entity = HTML_ENTITY_MAP.get(codepoint)
    if named_entity:
        html_entities.append(f"&{named_entity}")
    return html_entities


def get_utf8_dec_bytes(uni_char: str) -> list[int]:
    return list(uni_char.encode())


def get_utf8_hex_bytes(uni_char: str) -> list[str]:
    return [f"{x:02X}" for x in uni_char.encode()]


def get_utf8_value(uni_char: str) -> str:
    return " ".join(f"0x{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_uri_encoded_value(uni_char: str) -> str:
    return "".join(f"%{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_utf16_hex_bytes(uni_char: str) -> list[str]:
    bytes_8bit = [f"{x:02X}" for x in uni_char.encode("utf_16_be")]
    return (
        [f"{bytes_8bit[0]}{bytes_8bit[1]}"]
        if len(bytes_8bit) == 2
        else [f"{bytes_8bit[0]}{bytes_8bit[1]}", f"{bytes_8bit[2]}{bytes_8bit[3]}"]
        if len(bytes_8bit) == 4
        else []
    )


def get_utf16_dec_bytes(uni_char: str) -> list[int]:
    return [int(byte, 16) for byte in get_utf16_hex_bytes(uni_char)]


def get_utf16_value(uni_char: str) -> str:
    hex_bytes = [f"{x:02X}" for x in uni_char.encode("utf_16_be")]
    return (
        f"0x{hex_bytes[0]}{hex_bytes[1]}"
        if len(hex_bytes) == 2
        else f"0x{hex_bytes[0]}{hex_bytes[1]} 0x{hex_bytes[2]}{hex_bytes[3]}"
        if len(hex_bytes) == 4
        else ""
    )


def get_utf32_hex_bytes(uni_char: str) -> list[str]:
    return [f"{ord(uni_char):08X}"]


def get_utf32_dec_bytes(uni_char: str) -> list[int]:
    return [int(get_utf32_value(uni_char), 16)]


def get_utf32_value(uni_char: str) -> str:
    return f"0x{ord(uni_char):08X}"
