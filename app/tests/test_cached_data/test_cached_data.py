from app.data.cache import cached_data

TOTAL_CHARACTERS_IN_UNICODE_V15_0 = 149186


def test_total_number_of_unicode_characters():
    assert cached_data.official_number_of_unicode_characters == TOTAL_CHARACTERS_IN_UNICODE_V15_0
