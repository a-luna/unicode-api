from app.core.enums import UnicodeBlockName

CJK_UNIFIED_BLOCKS = [
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_B.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_C.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_D.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_E.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_F.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_G.block_id,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_H.block_id,
]

CJK_COMPATIBILITY_BLOCKS = [
    UnicodeBlockName.CJK_COMPATIBILITY_IDEOGRAPHS.block_id,
    UnicodeBlockName.CJK_COMPATIBILITY_IDEOGRAPHS_SUPPLEMENT.block_id,
]

TANGUT_BLOCKS = [
    UnicodeBlockName.TANGUT.block_id,
    UnicodeBlockName.TANGUT_SUPPLEMENT.block_id,
]

SINGLE_NO_NAME_BLOCKS = [
    UnicodeBlockName.HIGH_SURROGATES.block_id,
    UnicodeBlockName.HIGH_PRIVATE_USE_SURROGATES.block_id,
    UnicodeBlockName.LOW_SURROGATES.block_id,
    UnicodeBlockName.PRIVATE_USE_AREA.block_id,
    UnicodeBlockName.SUPPLEMENTARY_PRIVATE_USE_AREA_A.block_id,
    UnicodeBlockName.SUPPLEMENTARY_PRIVATE_USE_AREA_B.block_id,
]

NO_NAME_BLOCK_IDS = CJK_UNIFIED_BLOCKS + CJK_COMPATIBILITY_BLOCKS + TANGUT_BLOCKS + SINGLE_NO_NAME_BLOCKS
