from app.schemas.enums import CharPropertyGroup

CHARACTER_PROPERTIES = {
    "∑": {
        "character": "∑",
        "name": "N-ARY SUMMATION",
        "codepoint": "U+2211",
        "uriEncoded": "%E2%88%91",
        "block": "Mathematical Operators",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Math Symbol (Sm)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#8721;", "&#x2211;", "&sum;"],
        "utf8": "0xE2 0x88 0x91",
        "utf8HexBytes": ["E2", "88", "91"],
        "utf8DecBytes": ["226", "136", "145"],
        "utf16": "0x2211",
        "utf16HexBytes": ["2211"],
        "utf16DecBytes": ["8721"],
        "utf32": "0x00002211",
        "utf32HexBytes": ["00002211"],
        "utf32DecBytes": ["8721"],
        "bidirectionalClass": "Other Neutral (ON)",
        "bidirectionalIsMirrored": True,
        "bidirectionalMirroringGlyph": "",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Ambiguous (Alphabetic Or Ideographic) (AI)",
        "eastAsianWidth": "East Asian Ambiguous (A)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "math": True,
        "verticalOrientation": "Rotated 90 degrees clockwise (R)",
    },
    "🇦": {
        "character": "🇦",
        "name": "REGIONAL INDICATOR SYMBOL LETTER A",
        "codepoint": "U+1F1E6",
        "uriEncoded": "%F0%9F%87%A6",
        "block": "Enclosed Alphanumeric Supplement",
        "plane": "SMP",
        "age": "6.0",
        "generalCategory": "Other Symbol (So)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#127462;", "&#x1F1E6;"],
        "utf8": "0xF0 0x9F 0x87 0xA6",
        "utf8HexBytes": ["F0", "9F", "87", "A6"],
        "utf8DecBytes": ["240", "159", "135", "166"],
        "utf16": "0xD83C 0xDDE6",
        "utf16HexBytes": ["D83C", "DDE6"],
        "utf16DecBytes": ["55356", "56806"],
        "utf32": "0x0001F1E6",
        "utf32HexBytes": ["0001F1E6"],
        "utf32DecBytes": ["127462"],
        "bidirectionalClass": "Left To Right (L)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Unknown (XX)",
        "eastAsianWidth": "Neutral Not East Asian (N)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": True,
        "emoji": True,
        "emojiPresentation": True,
        "emojiComponent": True,
    },
    "🐍": {
        "character": "🐍",
        "name": "SNAKE",
        "codepoint": "U+1F40D",
        "uriEncoded": "%F0%9F%90%8D",
        "block": "Miscellaneous Symbols and Pictographs",
        "plane": "SMP",
        "age": "6.0",
        "generalCategory": "Other Symbol (So)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#128013;", "&#x1F40D;"],
        "utf8": "0xF0 0x9F 0x90 0x8D",
        "utf8HexBytes": ["F0", "9F", "90", "8D"],
        "utf8DecBytes": ["240", "159", "144", "141"],
        "utf16": "0xD83D 0xDC0D",
        "utf16HexBytes": ["D83D", "DC0D"],
        "utf16DecBytes": ["55357", "56333"],
        "utf32": "0x0001F40D",
        "utf32HexBytes": ["0001F40D"],
        "utf32DecBytes": ["128013"],
        "bidirectionalClass": "Other Neutral (ON)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Ideographic (ID)",
        "eastAsianWidth": "East Asian Wide (W)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "verticalOrientation": "Upright (U)",
        "emoji": True,
        "emojiPresentation": True,
        "extendedPictographic": True,
    },
    "穩": {
        "character": "穩",
        "name": "CJK UNIFIED IDEOGRAPH-7A69",
        "description": "stable, firm, solid, steady",
        "codepoint": "U+7A69",
        "uriEncoded": "%E7%A9%A9",
        "block": "CJK Unified Ideographs",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Other Letter (Lo)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#31337;", "&#x7A69;"],
        "ideoFrequency": 4,
        "ideoGradeLevel": 5,
        "rsCountUnicode": "115.14",
        "rsCountKangxi": "115.14",
        "totalStrokes": "19",
        "utf8": "0xE7 0xA9 0xA9",
        "utf8HexBytes": ["E7", "A9", "A9"],
        "utf8DecBytes": ["231", "169", "169"],
        "utf16": "0x7A69",
        "utf16HexBytes": ["7A69"],
        "utf16DecBytes": ["31337"],
        "utf32": "0x00007A69",
        "utf32HexBytes": ["00007A69"],
        "utf32DecBytes": ["31337"],
        "bidirectionalClass": "Left To Right (L)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Ideographic (ID)",
        "eastAsianWidth": "East Asian Wide (W)",
        "script": "Han (Hani)",
        "scriptExtensions": ["Han (Hani)"],
        "ideographic": True,
        "unifiedIdeograph": True,
        "simplifiedVariant": "U+7A33",
        "semanticVariant": "U+349A<kMatthews",
        "specializedSemanticVariant": "U+6587<kFenn",
        "hangul": "온:0N",
        "cantonese": "wan2",
        "mandarin": "wěn",
        "japaneseKun": "ODAYAKA",
        "japaneseOn": "ON",
        "vietnamese": "ủn",
        "alphabetic": True,
        "verticalOrientation": "Upright (U)",
    },
    "㑢": {
        "character": "㑢",
        "name": "CJK UNIFIED IDEOGRAPH-3462",
        "codepoint": "U+3462",
        "uriEncoded": "%E3%91%A2",
        "block": "CJK Unified Ideographs Extension A",
        "plane": "BMP",
        "age": "3.0",
        "generalCategory": "Other Letter (Lo)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#13410;", "&#x3462;"],
        "rsCountUnicode": "9.7",
        "totalStrokes": "9",
        "utf8": "0xE3 0x91 0xA2",
        "utf8HexBytes": ["E3", "91", "A2"],
        "utf8DecBytes": ["227", "145", "162"],
        "utf16": "0x3462",
        "utf16HexBytes": ["3462"],
        "utf16DecBytes": ["13410"],
        "utf32": "0x00003462",
        "utf32HexBytes": ["00003462"],
        "utf32DecBytes": ["13410"],
        "bidirectionalClass": "Left To Right (L)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Ideographic (ID)",
        "eastAsianWidth": "East Asian Wide (W)",
        "script": "Han (Hani)",
        "scriptExtensions": ["Han (Hani)"],
        "ideographic": True,
        "unifiedIdeograph": True,
        "cantonese": "koek3",
        "alphabetic": True,
        "verticalOrientation": "Upright (U)",
    },
    "(": {
        "character": "(",
        "name": "LEFT PARENTHESIS",
        "codepoint": "U+0028",
        "uriEncoded": "%28",
        "block": "Basic Latin",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Open Punctuation (Ps)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#40;", "&#x28;", "&lpar;"],
        "utf8": "0x28",
        "utf8HexBytes": ["28"],
        "utf8DecBytes": ["40"],
        "utf16": "0x0028",
        "utf16HexBytes": ["0028"],
        "utf16DecBytes": ["40"],
        "utf32": "0x00000028",
        "utf32HexBytes": ["00000028"],
        "utf32DecBytes": ["40"],
        "bidirectionalClass": "Other Neutral (ON)",
        "bidirectionalIsMirrored": True,
        "bidirectionalMirroringGlyph": ") (U+0029)",
        "pairedBracketType": "Open (o)",
        "pairedBracketProperty": ") (U+0029)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Opening Punctuation (OP)",
        "eastAsianWidth": "East Asian Narrow (Na)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "verticalOrientation": "Rotated 90 degrees clockwise (R)",
    },
    "￾": {
        "character": "￾",
        "name": "<noncharacter-FFFE>",
        "codepoint": "U+FFFE",
        "uriEncoded": "%EF%BF%BE",
        "block": "Specials",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Private Use (Co)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#65534;", "&#xFFFE;"],
        "utf8": "0xEF 0xBF 0xBE",
        "utf8HexBytes": ["EF", "BF", "BE"],
        "utf8DecBytes": ["239", "191", "190"],
        "utf16": "0xFFFE",
        "utf16HexBytes": ["FFFE"],
        "utf16DecBytes": ["65534"],
        "utf32": "0x0000FFFE",
        "utf32HexBytes": ["0000FFFE"],
        "utf32DecBytes": ["65534"],
        "bidirectionalClass": "Left To Right (L)",
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Unknown (XX)",
        "eastAsianWidth": "East Asian Ambiguous (A)",
        "script": "Unknown (Zzzz)",
        "scriptExtensions": ["Unknown (Zzzz)"],
        "indicSyllabicCategory": "",
        "indicMatraCategory": "",
        "indicPositionalCategory": "",
        "verticalOrientation": "Upright (U)",
    },
    "": {
        "character": "",
        "name": "<private-use-F800>",
        "codepoint": "U+F800",
        "uriEncoded": "%EF%A0%80",
        "block": "Private Use Area",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Private Use (Co)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#63488;", "&#xF800;"],
        "utf8": "0xEF 0xA0 0x80",
        "utf8HexBytes": ["EF", "A0", "80"],
        "utf8DecBytes": ["239", "160", "128"],
        "utf16": "0xF800",
        "utf16HexBytes": ["F800"],
        "utf16DecBytes": ["63488"],
        "utf32": "0x0000F800",
        "utf32HexBytes": ["0000F800"],
        "utf32DecBytes": ["63488"],
        "bidirectionalClass": "Left To Right (L)",
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Unknown (XX)",
        "eastAsianWidth": "East Asian Ambiguous (A)",
        "script": "Unknown (Zzzz)",
        "scriptExtensions": ["Unknown (Zzzz)"],
        "indicSyllabicCategory": "",
        "indicMatraCategory": "",
        "indicPositionalCategory": "",
        "verticalOrientation": "Upright (U)",
    },
    "\u0017": {
        "character": "␗",
        "name": "<control-0017> END OF TRANSMISSION BLOCK (ETB)",
        "codepoint": "U+0017",
        "uriEncoded": "%17",
        "block": "Basic Latin",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Control (Cc)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#23;", "&#x17;"],
        "utf8": "0x17",
        "utf8HexBytes": ["17"],
        "utf8DecBytes": ["23"],
        "utf16": "0x0017",
        "utf16HexBytes": ["0017"],
        "utf16DecBytes": ["23"],
        "utf32": "0x00000017",
        "utf32HexBytes": ["00000017"],
        "utf32DecBytes": ["23"],
        "bidirectionalClass": "Boundary Neutral (BN)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "lineBreak": "Attached Characters And Combining Marks (CM)",
        "eastAsianWidth": "Neutral Not East Asian (N)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "verticalOrientation": "Rotated 90 degrees clockwise (R)",
    },
}

VERBOSE_CHARACTER_PROPERTIES = {
    "∑": {
        "character": "∑",
        "name": "N-ARY SUMMATION",
        "codepoint": "U+2211",
        "uriEncoded": "%E2%88%91",
        "block": "Mathematical Operators",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Math Symbol (Sm)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#8721;", "&#x2211;", "&sum;"],
        "utf8": "0xE2 0x88 0x91",
        "utf8HexBytes": ["E2", "88", "91"],
        "utf8DecBytes": ["226", "136", "145"],
        "utf16": "0x2211",
        "utf16HexBytes": ["2211"],
        "utf16DecBytes": ["8721"],
        "utf32": "0x00002211",
        "utf32HexBytes": ["00002211"],
        "utf32DecBytes": ["8721"],
        "bidirectionalClass": "Other Neutral (ON)",
        "bidirectionalIsMirrored": True,
        "bidirectionalMirroringGlyph": "",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "∑ (U+2211)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Ambiguous (Alphabetic Or Ideographic) (AI)",
        "eastAsianWidth": "East Asian Ambiguous (A)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "∑ (U+2211)",
        "simpleLowercaseMapping": "∑ (U+2211)",
        "simpleTitlecaseMapping": "∑ (U+2211)",
        "simpleCaseFolding": "∑ (U+2211)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": True,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Rotated 90 degrees clockwise (R)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
    "🇦": {
        "character": "🇦",
        "name": "REGIONAL INDICATOR SYMBOL LETTER A",
        "codepoint": "U+1F1E6",
        "uriEncoded": "%F0%9F%87%A6",
        "block": "Enclosed Alphanumeric Supplement",
        "plane": "SMP",
        "age": "6.0",
        "generalCategory": "Other Symbol (So)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#127462;", "&#x1F1E6;"],
        "utf8": "0xF0 0x9F 0x87 0xA6",
        "utf8HexBytes": ["F0", "9F", "87", "A6"],
        "utf8DecBytes": ["240", "159", "135", "166"],
        "utf16": "0xD83C 0xDDE6",
        "utf16HexBytes": ["D83C", "DDE6"],
        "utf16DecBytes": ["55356", "56806"],
        "utf32": "0x0001F1E6",
        "utf32HexBytes": ["0001F1E6"],
        "utf32DecBytes": ["127462"],
        "bidirectionalClass": "Left To Right (L)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": "",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "🇦 (U+1F1E6)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Unknown (XX)",
        "eastAsianWidth": "Neutral Not East Asian (N)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "🇦 (U+1F1E6)",
        "simpleLowercaseMapping": "🇦 (U+1F1E6)",
        "simpleTitlecaseMapping": "🇦 (U+1F1E6)",
        "simpleCaseFolding": "🇦 (U+1F1E6)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": True,
        "emoji": True,
        "emojiPresentation": True,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": True,
        "extendedPictographic": False,
    },
    "🐍": {
        "character": "🐍",
        "name": "SNAKE",
        "codepoint": "U+1F40D",
        "uriEncoded": "%F0%9F%90%8D",
        "block": "Miscellaneous Symbols and Pictographs",
        "plane": "SMP",
        "age": "6.0",
        "generalCategory": "Other Symbol (So)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#128013;", "&#x1F40D;"],
        "utf8": "0xF0 0x9F 0x90 0x8D",
        "utf8HexBytes": ["F0", "9F", "90", "8D"],
        "utf8DecBytes": ["240", "159", "144", "141"],
        "utf16": "0xD83D 0xDC0D",
        "utf16HexBytes": ["D83D", "DC0D"],
        "utf16DecBytes": ["55357", "56333"],
        "utf32": "0x0001F40D",
        "utf32HexBytes": ["0001F40D"],
        "utf32DecBytes": ["128013"],
        "bidirectionalClass": "Other Neutral (ON)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": "",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "🐍 (U+1F40D)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Ideographic (ID)",
        "eastAsianWidth": "East Asian Wide (W)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "🐍 (U+1F40D)",
        "simpleLowercaseMapping": "🐍 (U+1F40D)",
        "simpleTitlecaseMapping": "🐍 (U+1F40D)",
        "simpleCaseFolding": "🐍 (U+1F40D)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": False,
        "emoji": True,
        "emojiPresentation": True,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": True,
    },
    "穩": {
        "character": "穩",
        "name": "CJK UNIFIED IDEOGRAPH-7A69",
        "description": "stable, firm, solid, steady",
        "codepoint": "U+7A69",
        "uriEncoded": "%E7%A9%A9",
        "block": "CJK Unified Ideographs",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Other Letter (Lo)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#31337;", "&#x7A69;"],
        "ideoFrequency": 4,
        "ideoGradeLevel": 5,
        "rsCountUnicode": "115.14",
        "rsCountKangxi": "115.14",
        "totalStrokes": "19",
        "utf8": "0xE7 0xA9 0xA9",
        "utf8HexBytes": ["E7", "A9", "A9"],
        "utf8DecBytes": ["231", "169", "169"],
        "utf16": "0x7A69",
        "utf16HexBytes": ["7A69"],
        "utf16DecBytes": ["31337"],
        "utf32": "0x00007A69",
        "utf32HexBytes": ["00007A69"],
        "utf32DecBytes": ["31337"],
        "bidirectionalClass": "Left To Right (L)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": "",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "穩 (U+7A69)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Ideographic (ID)",
        "eastAsianWidth": "East Asian Wide (W)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "穩 (U+7A69)",
        "simpleLowercaseMapping": "穩 (U+7A69)",
        "simpleTitlecaseMapping": "穩 (U+7A69)",
        "simpleCaseFolding": "穩 (U+7A69)",
        "script": "Han (Hani)",
        "scriptExtensions": ["Han (Hani)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": True,
        "unifiedIdeograph": True,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "traditionalVariant": "",
        "simplifiedVariant": "U+7A33",
        "zVariant": "",
        "compatibilityVariant": "",
        "semanticVariant": "U+349A<kMatthews",
        "specializedSemanticVariant": "U+6587<kFenn",
        "spoofingVariant": "",
        "accountingNumeric": "0",
        "primaryNumeric": "0",
        "otherNumeric": "0",
        "hangul": "온:0N",
        "cantonese": "wan2",
        "mandarin": "wěn",
        "japaneseKun": "ODAYAKA",
        "japaneseOn": "ON",
        "vietnamese": "ủn",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": True,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
    "㑢": {
        "character": "㑢",
        "name": "CJK UNIFIED IDEOGRAPH-3462",
        "description": "",
        "codepoint": "U+3462",
        "uriEncoded": "%E3%91%A2",
        "block": "CJK Unified Ideographs Extension A",
        "plane": "BMP",
        "age": "3.0",
        "generalCategory": "Other Letter (Lo)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#13410;", "&#x3462;"],
        "ideoFrequency": 0,
        "ideoGradeLevel": 0,
        "rsCountUnicode": "9.7",
        "rsCountKangxi": "",
        "totalStrokes": "9",
        "utf8": "0xE3 0x91 0xA2",
        "utf8HexBytes": ["E3", "91", "A2"],
        "utf8DecBytes": ["227", "145", "162"],
        "utf16": "0x3462",
        "utf16HexBytes": ["3462"],
        "utf16DecBytes": ["13410"],
        "utf32": "0x00003462",
        "utf32HexBytes": ["00003462"],
        "utf32DecBytes": ["13410"],
        "bidirectionalClass": "Left To Right (L)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": "",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "㑢 (U+3462)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Ideographic (ID)",
        "eastAsianWidth": "East Asian Wide (W)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "㑢 (U+3462)",
        "simpleLowercaseMapping": "㑢 (U+3462)",
        "simpleTitlecaseMapping": "㑢 (U+3462)",
        "simpleCaseFolding": "㑢 (U+3462)",
        "script": "Han (Hani)",
        "scriptExtensions": ["Han (Hani)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": True,
        "unifiedIdeograph": True,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "traditionalVariant": "",
        "simplifiedVariant": "",
        "zVariant": "",
        "compatibilityVariant": "",
        "semanticVariant": "",
        "specializedSemanticVariant": "",
        "spoofingVariant": "",
        "accountingNumeric": "0",
        "primaryNumeric": "0",
        "otherNumeric": "0",
        "hangul": "",
        "cantonese": "koek3",
        "mandarin": "",
        "japaneseKun": "",
        "japaneseOn": "",
        "vietnamese": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": True,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
    "(": {
        "character": "(",
        "name": "LEFT PARENTHESIS",
        "codepoint": "U+0028",
        "uriEncoded": "%28",
        "block": "Basic Latin",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Open Punctuation (Ps)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#40;", "&#x28;", "&lpar;"],
        "utf8": "0x28",
        "utf8HexBytes": ["28"],
        "utf8DecBytes": ["40"],
        "utf16": "0x0028",
        "utf16HexBytes": ["0028"],
        "utf16DecBytes": ["40"],
        "utf32": "0x00000028",
        "utf32HexBytes": ["00000028"],
        "utf32DecBytes": ["40"],
        "bidirectionalClass": "Other Neutral (ON)",
        "bidirectionalIsMirrored": True,
        "bidirectionalMirroringGlyph": ") (U+0029)",
        "bidirectionalControl": False,
        "pairedBracketType": "Open (o)",
        "pairedBracketProperty": ") (U+0029)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Opening Punctuation (OP)",
        "eastAsianWidth": "East Asian Narrow (Na)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "( (U+0028)",
        "simpleLowercaseMapping": "( (U+0028)",
        "simpleTitlecaseMapping": "( (U+0028)",
        "simpleCaseFolding": "( (U+0028)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Rotated 90 degrees clockwise (R)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
    "￾": {
        "character": "￾",
        "name": "<noncharacter-FFFE>",
        "codepoint": "U+FFFE",
        "uriEncoded": "%EF%BF%BE",
        "block": "Specials",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Private Use (Co)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#65534;", "&#xFFFE;"],
        "utf8": "0xEF 0xBF 0xBE",
        "utf8HexBytes": ["EF", "BF", "BE"],
        "utf8DecBytes": ["239", "191", "190"],
        "utf16": "0xFFFE",
        "utf16HexBytes": ["FFFE"],
        "utf16DecBytes": ["65534"],
        "utf32": "0x0000FFFE",
        "utf32HexBytes": ["0000FFFE"],
        "utf32DecBytes": ["65534"],
        "bidirectionalClass": "Left To Right (L)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": "￾ (U+FFFE)",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "",
        "numericValueParsed": 0.0,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "",
        "joiningControl": False,
        "lineBreak": "Unknown (XX)",
        "eastAsianWidth": "East Asian Ambiguous (A)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "",
        "simpleLowercaseMapping": "",
        "simpleTitlecaseMapping": "",
        "simpleCaseFolding": "",
        "script": "Unknown (Zzzz)",
        "scriptExtensions": ["Unknown (Zzzz)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "",
        "indicMatraCategory": "",
        "indicPositionalCategory": "",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
    "": {
        "character": "",
        "name": "<private-use-F800>",
        "codepoint": "U+F800",
        "uriEncoded": "%EF%A0%80",
        "block": "Private Use Area",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Private Use (Co)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#63488;", "&#xF800;"],
        "utf8": "0xEF 0xA0 0x80",
        "utf8HexBytes": ["EF", "A0", "80"],
        "utf8DecBytes": ["239", "160", "128"],
        "utf16": "0xF800",
        "utf16HexBytes": ["F800"],
        "utf16DecBytes": ["63488"],
        "utf32": "0x0000F800",
        "utf32HexBytes": ["0000F800"],
        "utf32DecBytes": ["63488"],
        "bidirectionalClass": "Left To Right (L)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": " (U+F800)",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "",
        "numericValueParsed": 0.0,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "",
        "joiningControl": False,
        "lineBreak": "Unknown (XX)",
        "eastAsianWidth": "East Asian Ambiguous (A)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "",
        "simpleLowercaseMapping": "",
        "simpleTitlecaseMapping": "",
        "simpleCaseFolding": "",
        "script": "Unknown (Zzzz)",
        "scriptExtensions": ["Unknown (Zzzz)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "",
        "indicMatraCategory": "",
        "indicPositionalCategory": "",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Upright (U)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
    "\u0017": {
        "character": "␗",
        "name": "<control-0017> END OF TRANSMISSION BLOCK (ETB)",
        "codepoint": "U+0017",
        "uriEncoded": "%17",
        "block": "Basic Latin",
        "plane": "BMP",
        "age": "1.1",
        "generalCategory": "Control (Cc)",
        "combiningClass": "Not Reordered (0)",
        "htmlEntities": ["&#23;", "&#x17;"],
        "utf8": "0x17",
        "utf8HexBytes": ["17"],
        "utf8DecBytes": ["23"],
        "utf16": "0x0017",
        "utf16HexBytes": ["0017"],
        "utf16DecBytes": ["23"],
        "utf32": "0x00000017",
        "utf32HexBytes": ["00000017"],
        "utf32DecBytes": ["23"],
        "bidirectionalClass": "Boundary Neutral (BN)",
        "bidirectionalIsMirrored": False,
        "bidirectionalMirroringGlyph": "",
        "bidirectionalControl": False,
        "pairedBracketType": "None (n)",
        "pairedBracketProperty": "\u0017 (U+0017)",
        "decompositionType": "None (none)",
        "NFC_QC": "Yes",
        "NFD_QC": "Yes",
        "NFKC_QC": "Yes",
        "NFKD_QC": "Yes",
        "numericType": "None (None)",
        "numericValue": "NaN",
        "numericValueParsed": None,
        "joiningType": "Non Joining (U)",
        "joiningGroup": "No_Joining_Group",
        "joiningControl": False,
        "lineBreak": "Attached Characters And Combining Marks (CM)",
        "eastAsianWidth": "Neutral Not East Asian (N)",
        "uppercase": False,
        "lowercase": False,
        "simpleUppercaseMapping": "\u0017 (U+0017)",
        "simpleLowercaseMapping": "\u0017 (U+0017)",
        "simpleTitlecaseMapping": "\u0017 (U+0017)",
        "simpleCaseFolding": "\u0017 (U+0017)",
        "script": "Common (Zyyy)",
        "scriptExtensions": ["Common (Zyyy)"],
        "hangulSyllableType": "Not Applicable (NA)",
        "indicSyllabicCategory": "Other",
        "indicMatraCategory": "NA",
        "indicPositionalCategory": "NA",
        "ideographic": False,
        "unifiedIdeograph": False,
        "radical": False,
        "equivalentUnifiedIdeograph": "",
        "dash": False,
        "hyphen": False,
        "quotationMark": False,
        "terminalPunctuation": False,
        "sentenceTerminal": False,
        "diacritic": False,
        "extender": False,
        "softDotted": False,
        "alphabetic": False,
        "math": False,
        "hexDigit": False,
        "asciiHexDigit": False,
        "defaultIgnorableCodePoint": False,
        "logicalOrderException": False,
        "prependedConcatenationMark": False,
        "whiteSpace": False,
        "verticalOrientation": "Rotated 90 degrees clockwise (R)",
        "regionalIndicator": False,
        "emoji": False,
        "emojiPresentation": False,
        "emojiModifier": False,
        "emojiModifierBase": False,
        "emojiComponent": False,
        "extendedPictographic": False,
    },
}


def get_all_prop_names():
    prop_names = {cls.normalized for cls in CharPropertyGroup if cls != CharPropertyGroup.NONE}
    prop_aliases = {cls.short_alias for cls in CharPropertyGroup if cls != CharPropertyGroup.NONE}
    prop_names.update(prop_aliases)
    return list(prop_names)


ALL_PROP_GROUP_NAMES = get_all_prop_names()

INVALID_PROP_GROUP_NAMES = {
    "detail": "3 values provided for the 'show_props' parameter are invalid: ['foo', 'bar', 'baz']"
}
