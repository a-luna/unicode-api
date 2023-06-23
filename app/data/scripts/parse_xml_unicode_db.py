import json
from pathlib import Path
from xml.dom import minidom

from app.core.config import PLANES_JSON
from app.core.result import Result
from app.data.constants import GENERIC_NAME_BLOCK_IDS, NULL_BLOCK, NULL_PLANE
from app.data.encoding import get_codepoint_string
from app.data.scripts.util import finish_task, start_task, update_progress

YES_NO_MAP = {"Y": True, "N": False}

CharDetailsDict = dict[str, bool | int | str]
BlockOrPlaneDetailsDict = dict[str, int | str]
AllParsedUnicodeData = tuple[list[BlockOrPlaneDetailsDict], list[BlockOrPlaneDetailsDict], list[CharDetailsDict]]


def parse_xml_unicode_database(xml_file: Path) -> Result[AllParsedUnicodeData]:
    spinner = start_task("Parsing Unicode XML database...")
    unicode_xml = minidom.parse(str(xml_file))  # nosec
    spinner.text = "Parsing Unicode plane and block data from XML database file..."
    all_planes: list[BlockOrPlaneDetailsDict] = json.loads(PLANES_JSON.read_text())
    all_blocks: list[BlockOrPlaneDetailsDict] = parse_unicode_block_data_from_xml(unicode_xml, all_planes)
    finish_task(spinner, True, "Successfully parsed Unicode plane and block data from XML database file!")
    all_chars: list[CharDetailsDict] = parse_unicode_character_data_from_xml(unicode_xml, all_blocks, all_planes)
    spinner = start_task("Counting number of defined characters in each block and plane...")
    count_defined_characters_per_block(all_chars, all_blocks)
    count_defined_characters_per_plane(all_blocks, all_planes)
    finish_task(spinner, True, "Successfully counted number of defined characters in each block and plane!")
    return Result.Ok((all_planes, all_blocks, all_chars))


def parse_unicode_block_data_from_xml(
    xml_doc: minidom.Document, parsed_planes: list[BlockOrPlaneDetailsDict]
) -> list[BlockOrPlaneDetailsDict]:
    all_blocks = xml_doc.getElementsByTagName("block")
    return [parse_block_details(id, block, parsed_planes) for id, block in enumerate(all_blocks, start=1)]


def parse_block_details(id: int, block_node, parsed_planes: list[BlockOrPlaneDetailsDict]):
    start = block_node.getAttribute("first-cp")
    finish = block_node.getAttribute("last-cp")
    start_dec = int(start, 16)
    finish_dec = int(finish, 16)
    plane = get_unicode_plane_containing_block_id(start_dec, finish_dec, parsed_planes)
    return {
        "id": id,
        "name": block_node.getAttribute("name"),
        "plane_number": plane["number"],
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


def parse_unicode_character_data_from_xml(
    xml_doc: minidom.Document,
    parsed_blocks: list[dict[str, str | int]],
    parsed_planes: list[dict[str, str | int]],
) -> list[CharDetailsDict]:
    spinner = start_task("")
    spinner.stop_and_persist("Parsing Unicode character data from XML database file...")
    char_nodes = xml_doc.getElementsByTagName("char")
    all_chars = [
        parse_character_details(char, parsed_blocks, parsed_planes, spinner, i, len(char_nodes))
        for (i, char) in enumerate(char_nodes, start=1)
        if "cp" in char.attributes  # type: ignore
    ]
    finish_task(spinner, True, "Successfully parsed Unicode character data from XML database file!")
    return all_chars


def parse_character_details(
    char_node: minidom.Element,
    parsed_blocks: list[dict[str, str | int]],
    parsed_planes: list[dict[str, str | int]],
    spinner,
    count,
    total,
) -> CharDetailsDict:
    codepoint = char_node.getAttribute("cp")
    codepoint_dec = int(codepoint, 16)
    block = get_unicode_block_containing_codepoint(codepoint_dec, parsed_blocks)
    plane = get_unicode_plane_containing_block_id(int(block["start_dec"]), int(block["finish_dec"]), parsed_planes)
    unihan = block["id"] in GENERIC_NAME_BLOCK_IDS
    parsed_char = {
        "character": chr(codepoint_dec),
        "name": get_character_name(char_node, codepoint, codepoint_dec, parsed_blocks),
        "codepoint": codepoint,
        "codepoint_dec": codepoint_dec,
        "block_id": block["id"],
        "plane_number": plane["number"],
        "unihan": unihan,
        "age": char_node.getAttribute("age"),
        "general_category": char_node.getAttribute("gc"),
        "combining_class": int(char_node.getAttribute("ccc")),
        "bidirectional_class": char_node.getAttribute("bc"),
        "bidirectional_is_mirrored": YES_NO_MAP[char_node.getAttribute("Bidi_M")],
        "bidirectional_mirroring_glyph": get_mapped_codepoint(char_node.getAttribute("bmg"), codepoint),
        "bidirectional_control": YES_NO_MAP[char_node.getAttribute("Bidi_C")],
        "paired_bracket_type": char_node.getAttribute("bpt"),
        "paired_bracket_property": get_mapped_codepoint(char_node.getAttribute("bpb"), codepoint),
        "decomposition_type": char_node.getAttribute("dt"),
        "NFC_QC": char_node.getAttribute("NFC_QC"),
        "NFD_QC": char_node.getAttribute("NFD_QC"),
        "NFKC_QC": char_node.getAttribute("NFKC_QC"),
        "NFKD_QC": char_node.getAttribute("NFKD_QC"),
        "numeric_type": char_node.getAttribute("nt"),
        "numeric_value": char_node.getAttribute("nv"),
        "numeric_value_parsed": parse_numeric_value(char_node.getAttribute("nv"), codepoint),
        "joining_type": char_node.getAttribute("jt"),
        "joining_group": char_node.getAttribute("jg"),
        "joining_control": YES_NO_MAP[char_node.getAttribute("Join_C")],
        "line_break": char_node.getAttribute("lb"),
        "east_asian_width": char_node.getAttribute("ea"),
        "uppercase": YES_NO_MAP[char_node.getAttribute("Upper")],
        "lowercase": YES_NO_MAP[char_node.getAttribute("Lower")],
        "simple_uppercase_mapping": get_mapped_codepoint(char_node.getAttribute("suc"), codepoint),
        "simple_lowercase_mapping": get_mapped_codepoint(char_node.getAttribute("slc"), codepoint),
        "simple_titlecase_mapping": get_mapped_codepoint(char_node.getAttribute("stc"), codepoint),
        "simple_case_folding": get_mapped_codepoint(char_node.getAttribute("scf"), codepoint),
        "script": char_node.getAttribute("sc"),
        "script_extensions": char_node.getAttribute("scx"),
        "hangul_syllable_type": char_node.getAttribute("hst"),
        "indic_syllabic_category": char_node.getAttribute("InSC"),
        "indic_matra_category": char_node.getAttribute("InMC") or "NA",
        "indic_positional_category": char_node.getAttribute("InPC"),
        "ideographic": get_bool_prop_value(char_node, "Ideo"),
        "unified_ideograph": get_bool_prop_value(char_node, "UIdeo"),
        "equivalent_unified_ideograph": char_node.getAttribute("EqUIdeo"),
        "radical": get_bool_prop_value(char_node, "Radical"),
        "dash": YES_NO_MAP[char_node.getAttribute("Dash")],
        "hyphen": YES_NO_MAP[char_node.getAttribute("Hyphen")],
        "quotation_mark": YES_NO_MAP[char_node.getAttribute("QMark")],
        "terminal_punctuation": YES_NO_MAP[char_node.getAttribute("Term")],
        "sentence_terminal": YES_NO_MAP[char_node.getAttribute("STerm")],
        "diacritic": YES_NO_MAP[char_node.getAttribute("Dia")],
        "extender": YES_NO_MAP[char_node.getAttribute("Ext")],
        "soft_dotted": YES_NO_MAP[char_node.getAttribute("SD")],
        "alphabetic": YES_NO_MAP[char_node.getAttribute("Alpha")],
        "math": YES_NO_MAP[char_node.getAttribute("Math")],
        "hex_digit": YES_NO_MAP[char_node.getAttribute("Hex")],
        "ascii_hex_digit": YES_NO_MAP[char_node.getAttribute("AHex")],
        "default_ignorable_code_point": YES_NO_MAP[char_node.getAttribute("DI")],
        "logical_order_exception": YES_NO_MAP[char_node.getAttribute("LOE")],
        "prepended_concatenation_mark": YES_NO_MAP[char_node.getAttribute("PCM")],
        "white_space": YES_NO_MAP[char_node.getAttribute("WSpace")],
        "vertical_orientation": char_node.getAttribute("vo"),
        "regional_indicator": YES_NO_MAP[char_node.getAttribute("RI")],
        "emoji": YES_NO_MAP[char_node.getAttribute("Emoji")],
        "emoji_presentation": YES_NO_MAP[char_node.getAttribute("EPres")],
        "emoji_modifier": YES_NO_MAP[char_node.getAttribute("EMod")],
        "emoji_modifier_base": YES_NO_MAP[char_node.getAttribute("EBase")],
        "emoji_component": YES_NO_MAP[char_node.getAttribute("EComp")],
        "extended_pictographic": YES_NO_MAP[char_node.getAttribute("ExtPict")],
    }

    if unihan:
        unihan_props = {
            "description": char_node.getAttribute("kDefinition"),
            "ideo_frequency": parse_numeric_value(char_node.getAttribute("kFrequency"), codepoint),
            "ideo_grade_level": parse_numeric_value(char_node.getAttribute("kGradeLevel"), codepoint),
            "rs_count_unicode": char_node.getAttribute("kRSUnicode"),
            "rs_count_kangxi": char_node.getAttribute("kRSKangXi"),
            "total_strokes": parse_numeric_value(char_node.getAttribute("kTotalStrokes"), codepoint),
            "traditional_variant": char_node.getAttribute("kTraditionalVariant"),
            "simplified_variant": char_node.getAttribute("kSimplifiedVariant"),
            "z_variant": char_node.getAttribute("kZVariant"),
            "compatibility_variant": char_node.getAttribute("kCompatibilityVariant"),
            "semantic_variant": char_node.getAttribute("kSemanticVariant"),
            "specialized_semantic_variant": char_node.getAttribute("kSpecializedSemanticVariant"),
            "spoofing_variant": char_node.getAttribute("kSpoofingVariant"),
            "accounting_numeric": char_node.getAttribute("kAccountingNumeric"),
            "primary_numeric": char_node.getAttribute("kPrimaryNumeric"),
            "other_numeric": char_node.getAttribute("kOtherNumeric"),
            "hangul": char_node.getAttribute("kHangul"),
            "cantonese": char_node.getAttribute("kCantonese"),
            "mandarin": char_node.getAttribute("kMandarin"),
            "japanese_kun": char_node.getAttribute("kJapaneseKun"),
            "japanese_on": char_node.getAttribute("kJapaneseOn"),
            "vietnamese": char_node.getAttribute("kVietnamese"),
        }
        parsed_char |= unihan_props

    update_progress(spinner, "Parsing Unicode character data from XML database file...", count, total)
    return parsed_char


def get_unicode_block_containing_codepoint(
    codepoint: int, parsed_blocks: list[dict[str, str | int]]
) -> dict[str, str | int]:
    found = [
        block
        for block in parsed_blocks
        if int(block["start_dec"]) <= codepoint and codepoint <= int(block["finish_dec"])
    ]
    return found[0] if found else NULL_BLOCK


def get_character_name(char_node, codepoint, codepoint_dec, block) -> str:
    name = char_node.getAttribute("na")
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


def get_bool_prop_value(char_node: minidom.Element, prop_name: str) -> bool:
    if (prop_value := char_node.getAttribute(prop_name)) != "":
        return YES_NO_MAP[prop_value]
    return False


def count_defined_characters_per_block(all_chars, all_blocks):
    char_map = {char["codepoint_dec"]: char for char in all_chars}
    for block in all_blocks:
        block["total_allocated"] = block["finish_dec"] - block["start_dec"] + 1
        block["total_defined"] = count_characters_in_range(char_map, block["start_dec"], block["finish_dec"])


def count_characters_in_range(char_map: dict[int, dict[str, str | int]], start: int, finish: int) -> int:
    chars_in_block = [char_map.get(codepoint) for codepoint in range(start, finish + 1) if codepoint in char_map]
    return len(chars_in_block)


def count_defined_characters_per_plane(all_blocks, all_planes):
    for plane in all_planes:
        plane["total_allocated"] = plane["finish_dec"] - plane["start_dec"] + 1
        plane["total_defined"] = sum(b["total_defined"] for b in all_blocks if b["plane_number"] == plane["number"])
