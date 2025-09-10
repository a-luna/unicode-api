from unicode_api.core.cache import cached_data

TOTAL_CHARACTERS_IN_UNICODE_V15_0 = 149186


def test_total_number_of_unicode_characters():
    assert cached_data.official_number_of_unicode_characters == TOTAL_CHARACTERS_IN_UNICODE_V15_0


def test_get_char_name_invalid_codepoint(client):
    codepoint = 1114112
    char_name = cached_data.get_character_name(codepoint)
    assert char_name == "Invalid Codepoint (U+110000)"


def test_get_unicode_version():
    version = "15.0.0"
    assert cached_data.unicode_version == version
