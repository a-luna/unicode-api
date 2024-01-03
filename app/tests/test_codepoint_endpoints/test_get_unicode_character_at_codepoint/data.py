CODEPOINT_24AF_RAW_HEX = {
    "character": "⒯",
    "name": "PARENTHESIZED LATIN SMALL LETTER T",
    "codepoint": "U+24AF",
    "uriEncoded": "%E2%92%AF",
}

CODEPOINT_24AF_WITH_PREFIX_1 = {
    "character": "⒯",
    "name": "PARENTHESIZED LATIN SMALL LETTER T",
    "codepoint": "U+24AF",
    "uriEncoded": "%E2%92%AF",
    "block": "Enclosed Alphanumerics",
    "plane": "BMP",
    "age": "1.1",
    "generalCategory": "Other Symbol (So)",
    "combiningClass": "Not Reordered (0)",
    "htmlEntities": ["&#9391;", "&#x24AF;"],
}

CODEPOINT_24AF_WITH_PREFIX_2 = {
    "character": "⒯",
    "name": "PARENTHESIZED LATIN SMALL LETTER T",
    "codepoint": "U+24AF",
    "uriEncoded": "%E2%92%AF",
    "block": "Enclosed Alphanumerics",
    "plane": "BMP",
    "age": "1.1",
    "generalCategory": "Other Symbol (So)",
    "combiningClass": "Not Reordered (0)",
    "htmlEntities": ["&#9391;", "&#x24AF;"],
    "utf8": "0xE2 0x92 0xAF",
    "utf8HexBytes": ["E2", "92", "AF"],
    "utf8DecBytes": [226, 146, 175],
    "utf16": "0x24AF",
    "utf16HexBytes": ["24AF"],
    "utf16DecBytes": [9391],
    "utf32": "0x000024AF",
    "utf32HexBytes": ["000024AF"],
    "utf32DecBytes": [9391],
    "bidirectionalClass": "Left To Right (L)",
    "decompositionType": "Otherwise Unspecified Compatibility Character (com)",
    "NFC_QC": "Yes",
    "NFD_QC": "Yes",
    "NFKC_QC": "No",
    "NFKD_QC": "No",
    "lineBreak": "Ambiguous (Alphabetic Or Ideographic) (AI)",
    "eastAsianWidth": "East Asian Ambiguous (A)",
    "script": "Common (Zyyy)",
    "scriptExtensions": ["Common (Zyyy)"],
    "verticalOrientation": "Upright (U)",
}

INVALID_HEX_DIGIT_1 = {
    "detail": "The value provided (0x24AZ) contains 1 invalid hexadecimal character: [Z]. The codepoint value must be expressed as a hexadecimal value within range 0000...10FFFF, optionally prefixed by 'U+'' or '0x'."
}

INVALID_HEX_DIGIT_2 = {
    "detail": "The value provided (maccaroni) contains 5 invalid hexadecimal characters: [i, m, n, o, r]. The codepoint value must be expressed as a hexadecimal value within range 0000...10FFFF, optionally prefixed by 'U+'' or '0x'."
}

INVALID_LEADING_ZEROS = {
    "detail": "The value provided (U+72) is invalid because Unicode codepoint values prefixed with 'U+' must contain at least 4 hexadecimal digits. The correct way to request the character assigned to codepoint 0x72 is with the value 'U+0072', which adds the necessary leading zeros."
}

INVALID_OUT_OF_RANGE = {
    "detail": "U+1234567 is not within the range of valid codepoints for Unicode characters (U+0000 to U+10FFFF)."
}

INVALID_PROP_NAME = {"detail": "1 value provided for the 'show_props' parameter is invalid: ['max']"}
