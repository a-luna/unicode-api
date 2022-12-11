from app.data.constants import HTML_ENTITY_MAP


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


def get_uri_encoded_value(uni_char: str) -> str:
    return "".join(f"%{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_utf8_value(uni_char: str) -> str:
    return " ".join(f"0x{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_utf16_value(uni_char: str) -> str:
    hex_bytes = [f"{x:02X}" for x in uni_char.encode("utf_16_be")]
    if len(hex_bytes) == 2:
        return f"0x{hex_bytes[0]}{hex_bytes[1]}"
    if len(hex_bytes) == 4:
        return f"0x{hex_bytes[0]}{hex_bytes[1]} 0x{hex_bytes[2]}{hex_bytes[3]}"


def get_utf32_value(uni_char: str) -> str:
    return f"0x{ord(uni_char):08X}"
