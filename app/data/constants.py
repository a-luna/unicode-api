MAX_CODEPOINT = 1114111

CJK_UNIFIED_BLOCKS = [121, 119, 316, 317, 318, 319, 320, 322, 323]
CJK_COMPATIBILITY_BLOCKS = [154, 321]
TANGUT_BLOCKS = [266, 269]
SINGLE_NO_NAME_BLOCKS = [150, 151, 152, 153, 326, 327]
SURROGATE_BLOCK_IDS = [150, 151, 152]
PRIVATE_USE_BLOCK_IDS = [153, 326, 327]

NULL_BLOCK = {
    "id": 0,
    "name": "",
    "plane_id": 0,
    "start": "",
    "start_dec": 0,
    "finish": "",
    "finish_dec": 0,
    "total_allocated": 0,
    "total_defined": 0,
}

NULL_PLANE = {
    "number": -1,
    "name": "Invalid Codepoint",
    "abbreviation": "N/A",
    "start": "",
    "start_dec": 0,
    "finish": "",
    "finish_dec": 0,
    "start_block_id": 0,
    "finish_block_id": 0,
    "total_allocated": 0,
    "total_defined": 0,
}
NON_CHARACTER_CODEPOINTS = [
    "FDD0",
    "FDD1",
    "FDD2",
    "FDD3",
    "FDD4",
    "FDD5",
    "FDD6",
    "FDD7",
    "FDD8",
    "FDD9",
    "FDDA",
    "FDDB",
    "FDDC",
    "FDDD",
    "FDDE",
    "FDDF",
    "FDE0",
    "FDE1",
    "FDE2",
    "FDE3",
    "FDE4",
    "FDE5",
    "FDE6",
    "FDE7",
    "FDE8",
    "FDE9",
    "FDEA",
    "FDEB",
    "FDEC",
    "FDED",
    "FDEE",
    "FDEF",
    "FFFE",
    "FFFF",
    "1FFFE",
    "1FFFF",
    "2FFFE",
    "2FFFF",
    "3FFFE",
    "3FFFF",
    "4FFFE",
    "4FFFF",
    "5FFFE",
    "5FFFF",
    "6FFFE",
    "6FFFF",
    "7FFFE",
    "7FFFF",
    "8FFFE",
    "8FFFF",
    "9FFFE",
    "9FFFF",
    "AFFFE",
    "AFFFF",
    "BFFFE",
    "BFFFF",
    "CFFFE",
    "CFFFF",
    "DFFFE",
    "DFFFF",
    "EFFFE",
    "EFFFF",
    "FFFFE",
    "FFFFF",
    "10FFFE",
    "10FFFF",
]