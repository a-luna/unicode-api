import json
from pathlib import Path

from lxml import etree
from lxml.etree import _Element, _ElementTree

from app.config.api_settings import UnicodeApiSettings
from app.constants import NULL_BLOCK, NULL_PLANE
from app.core.result import Result
from app.data.constants import NULL_BLOCK, NULL_PLANE
from app.data.encoding import get_codepoint_string
from app.data.scripts.script_types import AllParsedUnicodeData, BlockOrPlaneDetailsDict, CharDetailsDict
from app.data.util.spinners import Spinner

YES_NO_MAP = {"Y": "True", "N": "False"}


def parse_xml_unicode_database(config: UnicodeApiSettings) -> Result[AllParsedUnicodeData]:
    result = parse_etree_from_xml_file(config.XML_FILE)
    if result.failure or not result.value:
        return Result.Fail(result.error or "")
    unicode_xml = result.value

    (all_planes, all_blocks) = parse_unicode_plane_and_block_data_from_xml(unicode_xml, config)
    all_chars: list[CharDetailsDict] = parse_unicode_character_data_from_xml(unicode_xml, all_blocks, all_planes)
    spinner = Spinner()
    spinner.start("Counting number of defined characters in each block and plane...")
    count_defined_characters_per_block(all_chars, all_blocks)
    count_defined_characters_per_plane(all_blocks, all_planes)
    spinner.successful("Successfully counted number of defined characters in each block and plane!")
    return Result.Ok((all_planes, all_blocks, all_chars))


def parse_etree_from_xml_file(xml: Path) -> Result[_ElementTree]:
    spinner = Spinner()
    spinner.start("Parsing Unicode XML file to ETree..")
    try:
        unicode_xml = etree.parse(str(xml), parser=None)  # nosec
        spinner.successful("Successfully parsed Unicode XML database file!")
        return Result.Ok(unicode_xml)
    except Exception as ex:
        error = f"Error occurred parsing Unicode XML database file: {repr(ex)}"
        spinner.failed(error)
        return Result.Fail(error)


def parse_unicode_plane_and_block_data_from_xml(
    unicode_xml: _ElementTree, config: UnicodeApiSettings
) -> tuple[list[BlockOrPlaneDetailsDict], list[BlockOrPlaneDetailsDict]]:
    spinner = Spinner()
    spinner.start("Parsing Unicode plane and block data from XML database file...")
    all_planes: list[BlockOrPlaneDetailsDict] = json.loads(config.PLANES_JSON.read_text())
    all_blocks: list[BlockOrPlaneDetailsDict] = parse_unicode_block_data_from_xml(unicode_xml, all_planes)
    (all_planes, all_blocks) = get_block_range_for_each_plane(all_planes, all_blocks)
    spinner.successful("Successfully parsed Unicode plane and block data from XML database file!")
    return (all_planes, all_blocks)


def parse_unicode_block_data_from_xml(
    xml: _ElementTree, parsed_planes: list[BlockOrPlaneDetailsDict]
) -> list[BlockOrPlaneDetailsDict]:
    all_blocks = xml.findall(".//block", {None: "http://www.unicode.org/ns/2003/ucd/1.0"})
    return [parse_block_details(id, block, parsed_planes) for id, block in enumerate(all_blocks, start=1)]


def parse_block_details(id: int, block_node: _Element, parsed_planes: list[BlockOrPlaneDetailsDict]):
    start = block_node.get("first-cp", "0")
    finish = block_node.get("last-cp", "0")
    start_dec = int(start, 16)
    finish_dec = int(finish, 16)
    plane = get_unicode_plane_containing_block_id(start_dec, finish_dec, parsed_planes)
    return {
        "id": id,
        "name": block_node.get("name", ""),
        "plane_number": plane["number"],
        "plane_id": plane["id"],
        "start": f"{start_dec:04X}",
        "start_dec": start_dec,
        "finish": f"{finish_dec:04X}",
        "finish_dec": finish_dec,
        "total_allocated": finish_dec - start_dec + 1,
        "total_defined": 0,
    }


def get_unicode_plane_containing_block_id(
    start_dec: int, finish_dec: int, parsed_planes: list[BlockOrPlaneDetailsDict]
) -> BlockOrPlaneDetailsDict:
    found = [
        plane
        for plane in parsed_planes
        if int(plane["start_dec"]) <= start_dec and finish_dec <= int(plane["finish_dec"])
    ]
    return found[0] if found else NULL_PLANE


def get_block_range_for_each_plane(
    parsed_planes: list[BlockOrPlaneDetailsDict], parsed_blocks: list[BlockOrPlaneDetailsDict]
) -> tuple[list[BlockOrPlaneDetailsDict], list[BlockOrPlaneDetailsDict]]:
    for plane in parsed_planes:
        blocks_in_plane = [block for block in parsed_blocks if block["plane_id"] == plane["id"]]
        block_ids = sorted({block["id"] for block in blocks_in_plane if block and "id" in block})
        if block_ids:
            plane["start_block_id"] = block_ids[0]
            plane["finish_block_id"] = block_ids[-1]
    return (parsed_planes, parsed_blocks)


def parse_unicode_character_data_from_xml(
    xml: _ElementTree,
    blocks: list[BlockOrPlaneDetailsDict],
    planes: list[BlockOrPlaneDetailsDict],
) -> list[CharDetailsDict]:
    char_nodes = xml.findall(".//char", {None: "http://www.unicode.org/ns/2003/ucd/1.0"})
    spinner = Spinner()
    spinner.start("Parsing Unicode character data from XML database file...", total=len(char_nodes))
    all_chars = [parse_character_details(char, blocks, planes, spinner) for char in char_nodes if "cp" in char.keys()]  # noqa: SIM118
    spinner.successful("Successfully parsed Unicode character data from XML database file!")
    return all_chars


def parse_character_details(
    char_node: _Element,
    parsed_blocks: list[BlockOrPlaneDetailsDict],
    parsed_planes: list[BlockOrPlaneDetailsDict],
    spinner,
) -> tuple[CharDetailsDict, float]:
    codepoint = char_node.get("cp", "0")
    codepoint_dec = int(codepoint, 16)
    block = get_unicode_block_containing_codepoint(codepoint_dec, parsed_blocks)
    plane = [plane for plane in parsed_planes if plane["id"] == block["plane_id"]][0]
    unihan = char_is_unihan(str(block["name"]))
    parsed_char = {
        "character": chr(codepoint_dec),
        "name": get_character_name(char_node, codepoint, codepoint_dec, block),
        "codepoint": codepoint,
        "codepoint_dec": codepoint_dec,
        "block_id": block["id"],
        "plane_id": plane["id"],
        "plane_number": plane["number"],
        "_unihan": unihan,
        "_tangut": char_is_tangut(str(block["name"])),
        "age": char_node.get("age", "0"),
        "general_category": char_node.get("gc", "0"),
        "combining_class": int(char_node.get("ccc", "0")),
        "bidirectional_class": char_node.get("bc", "0"),
        "bidirectional_is_mirrored": YES_NO_MAP[char_node.get("Bidi_M", "N")],
        "bidirectional_mirroring_glyph": get_mapped_codepoint(char_node.get("bmg", ""), codepoint),
        "bidirectional_control": YES_NO_MAP[char_node.get("Bidi_C", "N")],
        "paired_bracket_type": char_node.get("bpt", ""),
        "paired_bracket_property": get_mapped_codepoint(char_node.get("bpb", ""), codepoint),
        "decomposition_type": char_node.get("dt", ""),
        "NFC_QC": char_node.get("NFC_QC", ""),
        "NFD_QC": char_node.get("NFD_QC", ""),
        "NFKC_QC": char_node.get("NFKC_QC", ""),
        "NFKD_QC": char_node.get("NFKD_QC", ""),
        "numeric_type": char_node.get("nt", ""),
        "numeric_value": char_node.get("nv", ""),
        "joining_type": char_node.get("jt", ""),
        "joining_group": char_node.get("jg", ""),
        "joining_control": YES_NO_MAP[char_node.get("Join_C", "N")],
        "line_break": char_node.get("lb", ""),
        "east_asian_width": char_node.get("ea", ""),
        "uppercase": YES_NO_MAP[char_node.get("Upper", "N")],
        "lowercase": YES_NO_MAP[char_node.get("Lower", "N")],
        "simple_uppercase_mapping": get_mapped_codepoint(char_node.get("suc", ""), codepoint),
        "simple_lowercase_mapping": get_mapped_codepoint(char_node.get("slc", ""), codepoint),
        "simple_titlecase_mapping": get_mapped_codepoint(char_node.get("stc", ""), codepoint),
        "simple_case_folding": get_mapped_codepoint(char_node.get("scf", ""), codepoint),
        "script": char_node.get("sc", ""),
        "script_extensions": char_node.get("scx", ""),
        "hangul_syllable_type": char_node.get("hst", ""),
        "indic_syllabic_category": char_node.get("InSC", ""),
        "indic_matra_category": char_node.get("InMC", "") or "NA",
        "indic_positional_category": char_node.get("InPC", ""),
        "ideographic": get_bool_prop_value(char_node, "Ideo"),
        "unified_ideograph": get_bool_prop_value(char_node, "UIdeo"),
        "equivalent_unified_ideograph": char_node.get("EqUIdeo", ""),
        "radical": get_bool_prop_value(char_node, "Radical"),
        "dash": YES_NO_MAP[char_node.get("Dash", "N")],
        "hyphen": YES_NO_MAP[char_node.get("Hyphen", "N")],
        "quotation_mark": YES_NO_MAP[char_node.get("QMark", "N")],
        "terminal_punctuation": YES_NO_MAP[char_node.get("Term", "N")],
        "sentence_terminal": YES_NO_MAP[char_node.get("STerm", "N")],
        "diacritic": YES_NO_MAP[char_node.get("Dia", "N")],
        "extender": YES_NO_MAP[char_node.get("Ext", "N")],
        "soft_dotted": YES_NO_MAP[char_node.get("SD", "N")],
        "alphabetic": YES_NO_MAP[char_node.get("Alpha", "N")],
        "math": YES_NO_MAP[char_node.get("Math", "N")],
        "hex_digit": YES_NO_MAP[char_node.get("Hex", "N")],
        "ascii_hex_digit": YES_NO_MAP[char_node.get("AHex", "N")],
        "default_ignorable_code_point": YES_NO_MAP[char_node.get("DI", "N")],
        "logical_order_exception": YES_NO_MAP[char_node.get("LOE", "N")],
        "prepended_concatenation_mark": YES_NO_MAP[char_node.get("PCM", "N")],
        "white_space": YES_NO_MAP[char_node.get("WSpace", "N")],
        "vertical_orientation": char_node.get("vo", ""),
        "regional_indicator": YES_NO_MAP[char_node.get("RI", "N")],
        "emoji": YES_NO_MAP[char_node.get("Emoji", "N")],
        "emoji_presentation": YES_NO_MAP[char_node.get("EPres", "N")],
        "emoji_modifier": YES_NO_MAP[char_node.get("EMod", "N")],
        "emoji_modifier_base": YES_NO_MAP[char_node.get("EBase", "N")],
        "emoji_component": YES_NO_MAP[char_node.get("EComp", "N")],
        "extended_pictographic": YES_NO_MAP[char_node.get("ExtPict", "N")],
    }

    if unihan:
        unihan_props = {
            "description": char_node.get("kDefinition", ""),
            "ideo_frequency": parse_numeric_value(char_node.get("kFrequency", ""), codepoint),
            "ideo_grade_level": parse_numeric_value(char_node.get("kGradeLevel", ""), codepoint),
            "rs_count_unicode": char_node.get("kRSUnicode", ""),
            "rs_count_kangxi": char_node.get("kRSKangXi", ""),
            "total_strokes": char_node.get("kTotalStrokes", ""),
            "traditional_variant": char_node.get("kTraditionalVariant", ""),
            "simplified_variant": char_node.get("kSimplifiedVariant", ""),
            "z_variant": char_node.get("kZVariant", ""),
            "compatibility_variant": char_node.get("kCompatibilityVariant", ""),
            "semantic_variant": char_node.get("kSemanticVariant", ""),
            "specialized_semantic_variant": char_node.get("kSpecializedSemanticVariant", ""),
            "spoofing_variant": char_node.get("kSpoofingVariant", ""),
            "accounting_numeric": char_node.get("kAccountingNumeric", ""),
            "primary_numeric": char_node.get("kPrimaryNumeric", ""),
            "other_numeric": char_node.get("kOtherNumeric", ""),
            "hangul": char_node.get("kHangul", ""),
            "cantonese": char_node.get("kCantonese", ""),
            "mandarin": char_node.get("kMandarin", ""),
            "japanese_kun": char_node.get("kJapaneseKun", ""),
            "japanese_on": char_node.get("kJapaneseOn", ""),
            "vietnamese": char_node.get("kVietnamese", ""),
        }
        parsed_char |= unihan_props

    spinner.increment()
    return parsed_char


def get_unicode_block_containing_codepoint(
    codepoint: int, parsed_blocks: list[BlockOrPlaneDetailsDict]
) -> BlockOrPlaneDetailsDict:
    found = [
        block
        for block in parsed_blocks
        if int(block["start_dec"]) <= codepoint and codepoint <= int(block["finish_dec"])
    ]
    return found[0] if found else NULL_BLOCK


def char_is_unihan(block_name: str) -> bool:
    return bool("cjk unified ideographs" in block_name.lower() or "cjk compatibility ideographs" in block_name.lower())


def char_is_tangut(block_name: str) -> bool:
    return bool("tangut" in block_name.lower())


def get_character_name(char_node: _Element, codepoint: str, codepoint_dec: int, block: BlockOrPlaneDetailsDict) -> str:
    name = char_node.get("na", "")
    return (
        f'Undefined Codepoint ({get_codepoint_string(codepoint_dec)}) (Reserved for {block["name"]})'
        if not codepoint
        else get_control_char_name(codepoint_dec)
        if not name
        else name.replace("#", codepoint)
        if "#" in name
        else name
    )


def get_control_char_name(codepoint: int) -> str:
    control_char_names = {
        0: " NULL (NUL)",
        1: " START OF HEADING (SOH)",
        2: " START OF TEXT (STX)",
        3: " END OF TEXT (ETX)",
        4: " END OF TRANSMISSION (EOT)",
        5: " ENQUIRY (ENQ)",
        6: " ACKNOWLEDGE (ACK)",
        7: " BELL (BEL)",
        8: " BACKSPACE (BS)",
        9: " HORIZONTAL TABULATION (HT TAB)",
        10: " END OF LINE (EOL LF, NL)",
        11: " VERTICAL TABULATION (VT)",
        12: " FORM FEED (FF)",
        13: " CARRIAGE RETURN (CR)",
        14: " SHIFT OUT (SO)",
        15: " SHIFT IN (SI)",
        16: " DATA LINK ESCAPE (DLE)",
        17: " DEVICE CONTROL ONE (DC1)",
        18: " DEVICE CONTROL TWO (DC2)",
        19: " DEVICE CONTROL THREE (DC3)",
        20: " DEVICE CONTROL FOUR (DC4)",
        21: " NEGATIVE ACKNOWLEDGE (NAK)",
        22: " SYNCHRONOUS IDLE (SYN)",
        23: " END OF TRANSMISSION BLOCK (ETB)",
        24: " CANCEL (CAN)",
        25: " END OF MEDIUM (EOM)",
        26: " SUBSTITUTE (SUB)",
        27: " ESCAPE (ESC)",
        28: " FILE SEPARATOR (FS)",
        29: " GROUP SEPARATOR (GS)",
        30: " RECORD SEPARATOR (RS)",
        31: " UNIT SEPARATOR (US)",
        127: " DELETE (DEL)",
        128: " PADDING CHARACTER (PAD)",
        129: " HIGH OCTET PRESET (HOP)",
        130: " BREAK PERMITTED HERE (BPH)",
        131: " NO BREAK HERE (NBH)",
        132: " INDEX (IND)",
        133: " NEXT LINE (NEL)",
        134: " START OF SELECTED AREA (SSA)",
        135: " END OF SELECTED AREA (ESA)",
        136: " CHARACTER TABULATION SET (HTS)",
        137: " CHARACTER TABULATION WITH JUSTIFICATION (HTJ)",
        138: " LINE TABULATION SET (VTS)",
        139: " PARTIAL LINE FORWARD (PLD)",
        140: " PARTIAL LINE BACKWARD (PLU)",
        141: " REVERSE LINE FEED (RI)",
        142: " SINGLE SHIFT TWO (SS2)",
        143: " SINGLE SHIFT THREE (SS3)",
        144: " DEVICE CONTROL STRING (DCS)",
        145: " PRIVATE USE ONE (PU1)",
        146: " PRIVATE USE TWO (PU2)",
        147: " SET TRANSMIT STATE (STS)",
        148: " CANCEL CHARACTER (CCH)",
        149: " MESSAGE WAITING (MW)",
        150: " START OF GUARDED AREA (SPA)",
        151: " END OF GUARDED AREA (EPA)",
        152: " START OF STRING (SOS)",
        153: " SINGLE GRAPHIC CHARACTER INTRODUCER (SGC)",
        154: " SINGLE CHARACTER INTRODUCER (SCI)",
        155: " CONTROL SEQUENCE INTRODUCER (CSI)",
        156: " STRING TERMINATOR (ST)",
        157: " OPERATING SYSTEM COMMAND (OSC)",
        158: " PRIVACY MESSAGE (PM)",
        159: " APPLICATION PROGRAM COMMAND (APC)",
    }
    return f'<control-{codepoint:04X}>{control_char_names.get(codepoint, "")}'


def get_mapped_codepoint(prop_value: str, codepoint_hex: str) -> str:
    return codepoint_hex if prop_value == "#" else prop_value if prop_value else ""


def get_decomposition_mapping(decomposition_mapping: str, codepoint: int) -> str:
    return decomposition_mapping if decomposition_mapping != "#" else f"{codepoint:04X}"


def parse_numeric_value(numeric_value: str, codepoint: str) -> int | float | None:
    if not numeric_value or numeric_value == "NaN":
        return None
    if "/" in numeric_value:
        [num, dom] = numeric_value.split("/", 1)
        return int(num) / float(dom)
    try:
        return int(numeric_value)
    except ValueError as ex:
        print(f"Error parsing numeric_value for codepoint {codepoint}: {repr(ex)}")
        return None


def get_bool_prop_value(char_node: _Element, prop_name: str) -> int:
    if prop_value := char_node.get(prop_name, "N"):
        return YES_NO_MAP[prop_value]
    return 0


def count_defined_characters_per_block(all_chars: list[CharDetailsDict], all_blocks: list[BlockOrPlaneDetailsDict]):
    char_map = {int(char["codepoint_dec"]): char for char in all_chars}
    for block in all_blocks:
        block["total_allocated"] = int(block["finish_dec"]) - int(block["start_dec"]) + 1
        block["total_defined"] = count_defined_characters_in_range(
            char_map, int(block["start_dec"]), int(block["finish_dec"])
        )


def count_defined_characters_in_range(char_map: dict[int, BlockOrPlaneDetailsDict], start: int, finish: int) -> int:
    return len([codepoint for codepoint in range(start, finish + 1) if codepoint in char_map])


def count_defined_characters_per_plane(
    all_blocks: list[BlockOrPlaneDetailsDict], all_planes: list[BlockOrPlaneDetailsDict]
):
    for plane in all_planes:
        plane["total_allocated"] = int(plane["finish_dec"]) - int(plane["start_dec"]) + 1
        plane["total_defined"] = sum(int(b["total_defined"]) for b in all_blocks if b["plane_id"] == plane["id"])
