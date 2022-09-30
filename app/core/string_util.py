def get_codepoint_string(codepoint: int) -> str:
    return f"U+{hex(codepoint)[2:].upper()}"
