import json
from pathlib import Path
from xml.dom import minidom

from app.core.config import PLANES_JSON
from app.core.result import Result
from app.core.util import get_codepoint_string
from app.data.categories import (
    get_bidi_bracket_type,
    get_bidirectional_category,
    get_combining_class_category,
    get_decomposition_type,
    get_east_asian_width_type,
    get_general_category,
    get_hangle_syllable_type,
    get_indic_property_value,
    get_joining_type,
    get_line_break_type,
    get_numeric_type,
    get_script_code_value,
    get_script_ext_code_values,
    get_vertical_orientation_type,
)
from app.data.constants import NULL_BLOCK, NULL_PLANE
from app.data.encoding import (
    get_html_entities,
    get_uri_encoded_value,
    get_utf8_dec_bytes,
    get_utf8_hex_bytes,
    get_utf8_value,
    get_utf16_value,
    get_utf32_value,
)

YES_NO_MAP = {"Y": True, "N": False}

CharDetailsDict = dict[str, bool | int | str | list[str] | list[int]]


def parse_unicode_data_from_xml(
    xml_file: Path,
) -> Result[tuple[list[dict[str, int | str]], list[dict[str, int | str]], list[CharDetailsDict]]]:
    unicode_xml = minidom.parse(str(xml_file))
    all_planes: list[dict[str, int | str]] = json.loads(PLANES_JSON.read_text())
    all_blocks: list[dict[str, int | str]] = parse_unicode_block_data_from_xml(unicode_xml, all_planes)
    all_chars: list[CharDetailsDict] = parse_unicode_character_data_from_xml(unicode_xml, all_blocks, all_planes)
    count_defined_characters_per_block(all_chars, all_blocks)
    count_defined_characters_per_plane(all_blocks, all_planes)
    return Result.Ok((all_planes, all_blocks, all_chars))


def parse_unicode_block_data_from_xml(
    xml_doc: minidom.Document, parsed_planes: list[dict[str, int | str]]
) -> list[dict[str, int | str]]:
    all_blocks = xml_doc.getElementsByTagName("block")
    return [parse_block_details(id, block, parsed_planes) for id, block in enumerate(all_blocks, start=1)]


def parse_block_details(id: int, block_node, parsed_planes: list[dict[str, int | str]]):
    start = block_node.getAttribute("first-cp")
    finish = block_node.getAttribute("last-cp")
    start_dec = int(start, 16)
    finish_dec = int(finish, 16)
    plane = get_unicode_plane_containing_block_id(id, parsed_planes)
    return {
        "id": id,
        "name": block_node.getAttribute("name"),
        "plane": plane["abbreviation"],
        "start": get_codepoint_string(start_dec),
        "start_dec": start_dec,
        "finish": get_codepoint_string(finish_dec),
        "finish_dec": finish_dec,
        "total_allocated": finish_dec - start_dec + 1,
        "total_defined": 0,
    }


def get_unicode_plane_containing_block_id(
    block_id: int, parsed_planes: list[dict[str, int | str]]
) -> dict[str, int | str]:
    found = [
        plane for plane in parsed_planes if plane["start_block_id"] <= block_id and block_id <= plane["finish_block_id"]
    ]
    return found[0] if found else NULL_PLANE


def parse_unicode_character_data_from_xml(
    xml_doc: minidom.Document,
    parsed_blocks: list[dict[str, str | int]],
    parsed_planes: list[dict[str, str | int]],
) -> list[dict[str, str | int]]:
    all_chars = xml_doc.getElementsByTagName("char")
    return [
        parse_character_details(char, parsed_blocks, parsed_planes) for char in all_chars if "cp" in char.attributes
    ]


def parse_character_details(
    char_node: minidom.Node, parsed_blocks: list[dict[str, str | int]], parsed_planes: list[dict[str, str | int]]
) -> CharDetailsDict:
    codepoint = char_node.getAttribute("cp")
    codepoint_dec = int(codepoint, 16)
    block = get_unicode_block_containing_codepoint(codepoint_dec, parsed_blocks)
    plane = get_unicode_plane_containing_block_id(block["id"], parsed_planes)
    char_details = {
        "character": chr(codepoint_dec),
        "name": get_character_name(char_node, codepoint_dec, parsed_blocks),
        "codepoint": get_codepoint_string(codepoint_dec),
        "codepoint_dec": codepoint_dec,
        "block_id": block["id"],
        "block": block["name"],
        "plane_number": plane["number"],
        "plane": f'{plane["name"]} ({plane["abbreviation"]})',
        "html_entities": get_html_entities(codepoint_dec),
        "uri_encoded": get_uri_encoded_value(chr(codepoint_dec)),
        "utf8_dec_bytes": get_utf8_dec_bytes(chr(codepoint_dec)),
        "utf8_hex_bytes": get_utf8_hex_bytes(chr(codepoint_dec)),
        "utf8": get_utf8_value(chr(codepoint_dec)),
        "utf16": get_utf16_value(chr(codepoint_dec)),
        "utf32": get_utf32_value(chr(codepoint_dec)),
        "age": char_node.getAttribute("age"),
        "general_category_value": char_node.getAttribute("gc"),
        "general_category": get_general_category(char_node.getAttribute("gc")),
        "combining_class_value": int(char_node.getAttribute("ccc")),
        "combining_class": get_combining_class_category(int(char_node.getAttribute("ccc"))),
        "bidirectional_class_value": char_node.getAttribute("bc"),
        "bidirectional_class": get_bidirectional_category(char_node.getAttribute("bc")),
        "bidirectional_is_mirrored": YES_NO_MAP[char_node.getAttribute("Bidi_M")],
        "bidirectional_mirroring_glyph": get_mapped_codepoint(char_node.getAttribute("bmg"), codepoint),
        "bidirectional_control": YES_NO_MAP[char_node.getAttribute("Bidi_C")],
        "paired_bracket_type_value": char_node.getAttribute("bpt"),
        "paired_bracket_type": get_bidi_bracket_type(char_node.getAttribute("bpt")),
        "paired_bracket_property": get_mapped_codepoint(char_node.getAttribute("bpb"), codepoint),
        "decomposition_type_value": char_node.getAttribute("dt"),
        "decomposition_type": get_decomposition_type(char_node.getAttribute("dt")),
        "decomposition_mapping": get_decomposition_mapping(char_node.getAttribute("dm"), codepoint_dec),
        "composition_exclusion": YES_NO_MAP[char_node.getAttribute("CE")],
        "full_composition_exclusion": YES_NO_MAP[char_node.getAttribute("Comp_Ex")],
        "numeric_type_value": get_numeric_type(char_node.getAttribute("nt")),
        "numeric_type": char_node.getAttribute("nt"),
        "numeric_value": char_node.getAttribute("nv"),
        "joining_class_value": char_node.getAttribute("jt"),
        "joining_class": get_joining_type(char_node.getAttribute("jt")),
        "joining_group": char_node.getAttribute("jg"),
        "joining_control": YES_NO_MAP[char_node.getAttribute("Join_C")],
        "line_break_value": char_node.getAttribute("lb"),
        "line_break": get_line_break_type(char_node.getAttribute("lb")),
        "east_asian_width_value": char_node.getAttribute("ea"),
        "east_asian_width": get_east_asian_width_type(char_node.getAttribute("ea")),
        "uppercase": YES_NO_MAP[char_node.getAttribute("Upper")],
        "lowercase": YES_NO_MAP[char_node.getAttribute("Lower")],
        "simple_uppercase_mapping": char_node.getAttribute("suc"),
        "simple_lowercase_mapping": char_node.getAttribute("slc"),
        "simple_titlecase_mapping": char_node.getAttribute("stc"),
        "simple_case_folding": char_node.getAttribute("scf"),
        "other_uppercase": YES_NO_MAP[char_node.getAttribute("OUpper")],
        "other_lowercase": YES_NO_MAP[char_node.getAttribute("OLower")],
        "other_uppercase_mapping": char_node.getAttribute("uc"),
        "other_lowercase_mapping": char_node.getAttribute("lc"),
        "other_titlecase_mapping": char_node.getAttribute("tc"),
        "other_case_folding": char_node.getAttribute("cf"),
        "script_value": char_node.getAttribute("sc"),
        "script": get_script_code_value(char_node.getAttribute("sc")),
        "script_extension_value": char_node.getAttribute("scx"),
        "script_extension": get_script_ext_code_values(char_node.getAttribute("scx")),
        "hangul_syllable_type_value": char_node.getAttribute("hst"),
        "hangul_syllable_type": get_hangle_syllable_type(char_node.getAttribute("hst")),
        "jamo_short_name": char_node.getAttribute("JSN"),
        "indic_syllabic_category_value": char_node.getAttribute("InSC"),
        "indic_syllabic_category": get_indic_property_value(char_node.getAttribute("InSC")),
        "indic_matra_category_value": char_node.getAttribute("InMC") or "NA",
        "indic_matra_category": get_indic_property_value(char_node.getAttribute("InMC") or "NA"),
        "indic_positional_category_value": char_node.getAttribute("InPC"),
        "indic_positional_category": get_indic_property_value(char_node.getAttribute("InPC")),
        "dash": YES_NO_MAP[char_node.getAttribute("Dash")],
        "hyphen": YES_NO_MAP[char_node.getAttribute("Hyphen")],
        "quotation_mark": YES_NO_MAP[char_node.getAttribute("QMark")],
        "terminal_punctuation": YES_NO_MAP[char_node.getAttribute("Term")],
        "sentence_terminal": YES_NO_MAP[char_node.getAttribute("STerm")],
        "diacritic": YES_NO_MAP[char_node.getAttribute("Dia")],
        "extender": YES_NO_MAP[char_node.getAttribute("Ext")],
        "soft_dotted": YES_NO_MAP[char_node.getAttribute("PCM")],
        "alphabetic": YES_NO_MAP[char_node.getAttribute("SD")],
        "other_alphabetic": YES_NO_MAP[char_node.getAttribute("Alpha")],
        "math": YES_NO_MAP[char_node.getAttribute("OAlpha")],
        "other_math": YES_NO_MAP[char_node.getAttribute("Math")],
        "hex_digit": YES_NO_MAP[char_node.getAttribute("OMath")],
        "ascii_hex_digit": YES_NO_MAP[char_node.getAttribute("Hex")],
        "default_ignorable_code_point": YES_NO_MAP[char_node.getAttribute("AHex")],
        "other_default_ignorable_code_point": YES_NO_MAP[char_node.getAttribute("DI")],
        "logical_order_exception": YES_NO_MAP[char_node.getAttribute("ODI")],
        "prepended_concatenation_mark": YES_NO_MAP[char_node.getAttribute("LOE")],
        "white_space": YES_NO_MAP[char_node.getAttribute("WSpace")],
        "vertical_orientation_value": char_node.getAttribute("vo"),
        "vertical_orientation": get_vertical_orientation_type(char_node.getAttribute("vo")),
        "regional_indicator": YES_NO_MAP[char_node.getAttribute("RI")],
        "emoji": YES_NO_MAP[char_node.getAttribute("Emoji")],
        "emoji_presentation": YES_NO_MAP[char_node.getAttribute("EPres")],
        "emoji_modifier": YES_NO_MAP[char_node.getAttribute("EMod")],
        "emoji_modifier_base": YES_NO_MAP[char_node.getAttribute("EBase")],
        "emoji_component": YES_NO_MAP[char_node.getAttribute("EComp")],
        "extended_pictographic": YES_NO_MAP[char_node.getAttribute("ExtPict")],
    }
    return prune_superfluous_character_properties(char_details)


def get_unicode_block_containing_codepoint(codepoint, parsed_blocks):
    found = [block for block in parsed_blocks if block["start_dec"] <= codepoint and codepoint <= block["finish_dec"]]
    return found[0] if found else NULL_BLOCK


def get_character_name(char_node, codepoint, block) -> str:
    name = char_node.getAttribute("na")
    return (
        f'Undefined Codepoint ({get_codepoint_string(codepoint)}) (Reserved for {block["name"]})'
        if not char_node.getAttribute("cp")
        else get_control_char_name(codepoint)
        if not name
        else name.replace("#", char_node.getAttribute("cp"))
        if "#" in name
        else name
    )


def get_control_char_name(codepoint: int) -> str:
    control_char_names = {
        0: "<control>: NULL",
        1: "<control>: START OF HEADING",
        2: "<control>: START OF TEXT",
        3: "<control>: END OF TEXT",
        4: "<control>: END OF TRANSMISSION",
        5: "<control>: ENQUIRY",
        6: "<control>: ACKNOWLEDGE",
        7: "<control>: BELL",
        8: "<control>: BACKSPACE",
        9: "<control>: HORIZONTAL TABULATION",
        10: "<control>: LINE FEED",
        11: "<control>: VERTICAL TABULATION",
        12: "<control>: FORM FEED",
        13: "<control>: CARRIAGE RETURN",
        14: "<control>: SHIFT OUT",
        15: "<control>: SHIFT IN",
        16: "<control>: DATA LINK ESCAPE",
        17: "<control>: DEVICE CONTROL ONE",
        18: "<control>: DEVICE CONTROL TWO",
        19: "<control>: DEVICE CONTROL THREE",
        20: "<control>: DEVICE CONTROL FOUR",
        21: "<control>: NEGATIVE ACKNOWLEDGE",
        22: "<control>: SYNCHRONOUS IDLE",
        23: "<control>: END OF TRANSMISSION BLOCK",
        24: "<control>: CANCEL",
        25: "<control>: END OF MEDIUM",
        26: "<control>: SUBSTITUTE",
        27: "<control>: ESCAPE",
        28: "<control>: FILE SEPARATOR",
        29: "<control>: GROUP SEPARATOR",
        30: "<control>: RECORD SEPARATOR",
        31: "<control>: UNIT SEPARATOR",
    }
    return control_char_names.get(codepoint, "")


def get_mapped_codepoint(prop_value: str, codepoint_hex: str) -> str:
    return f"U+{codepoint_hex}" if prop_value == "#" else f"U+{prop_value}" if prop_value else ""


def get_decomposition_mapping(decomposition_mapping: str, codepoint: int) -> list[str]:
    if decomposition_mapping == "#":
        decomposition_mapping = f"{codepoint:04X}"
    return [f"{chr(int(cp, 16))} (U+{cp})" for cp in decomposition_mapping.split(" ")]


def prune_superfluous_character_properties(char_details: CharDetailsDict) -> CharDetailsDict:
    if not char_details["bidirectional_is_mirrored"]:
        char_details.pop("bidirectional_mirroring_glyph")
    if "None" in char_details["paired_bracket_type"]:
        char_details.pop("paired_bracket_property")
    if "None" in char_details["decomposition_type"]:
        char_details.pop("decomposition_mapping")
    if char_details["numeric_value"] == "NaN":
        char_details.pop("numeric_value")
    return char_details


def count_defined_characters_per_block(all_chars, all_blocks):
    char_map = {char["codepoint_dec"]: char for char in all_chars}
    for block in all_blocks:
        block["total_allocated"] = block["finish_dec"] - block["start_dec"] + 1
        block["total_defined"] = count_characters_in_range(char_map, block["start_dec"], block["finish_dec"])


def count_characters_in_range(
    char_map: dict[int, dict[str, str | int]], start: int, finish: int
) -> list[dict[str, str | int]]:
    chars_in_block = [char_map.get(codepoint) for codepoint in range(start, finish + 1) if codepoint in char_map]
    return len(chars_in_block)


def count_defined_characters_per_plane(all_blocks, all_planes):
    for plane in all_planes:
        plane["total_allocated"] = plane["finish_dec"] - plane["start_dec"] + 1
        plane["total_defined"] = sum(b["total_defined"] for b in all_blocks if b["plane"] == plane["abbreviation"])
