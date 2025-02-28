import json
from collections.abc import Sequence
from pathlib import Path
from textwrap import dedent, fill
from typing import TYPE_CHECKING, Any

import lxml.etree as etree
from lxml.etree import _Element, _ElementTree
from pydantic import ValidationError

import app.db.models as db
from app.config.api_settings import UnicodeApiSettings
from app.constants import PROP_GROUP_INVALID_FOR_VERSION_ROW_ID
from app.core.cache import NULL_BLOCK, NULL_PLANE
from app.core.encoding import get_codepoint_string
from app.core.result import Result
from app.data.scripts.script_types import AllParsedUnicodeData, CharUnicodeModel, UnicodeModel
from app.data.util.spinners import Spinner
from app.models.util import normalize_string_lm3

if TYPE_CHECKING:  # pragma: no cover
    from app.custom_types import UnicodePropertyGroupMap, UnicodePropertyGroupValues

ERROR_MESSAGE_MAX_WIDTH = 80
YES_NO_MAP = {"Y": True, "N": False}


def parse_xml_unicode_database(settings: UnicodeApiSettings) -> Result[AllParsedUnicodeData]:
    result = parse_etree_from_xml_file(settings.XML_FILE)
    if result.failure:
        return Result.Fail(result.error)
    if not (unicode_xml := result.value):
        return Result.Fail("Error parsing Unicode XML database file: No data found!")

    result = parse_unicode_plane_and_block_data_from_xml(unicode_xml, settings)
    if result.failure:
        return Result.Fail(result.error)
    if not result.value:
        return Result.Fail("Error parsing Unicode plane and block data from XML database file: No data found!")
    planes, blocks = result.value

    result = parse_unicode_character_data_from_xml(settings, unicode_xml, blocks, planes)
    if result.failure:
        return Result.Fail(result.error)
    if not result.value:
        return Result.Fail("Error parsing Unicode character data from XML database file: No data found!")
    non_unihan_chars, tangut_chars, unihan_chars = result.value

    all_parsed_data = (planes, blocks, non_unihan_chars, tangut_chars, unihan_chars)
    return Result.Ok(finalize_all_parsed_unicode_data(settings, all_parsed_data))


def parse_etree_from_xml_file(xml: Path) -> Result[_ElementTree]:
    spinner = Spinner()
    spinner.start("Parsing Unicode XML file to ETree..")
    try:
        unicode_xml: _ElementTree = etree.parse(str(xml), parser=None)  # nosec
        spinner.successful("Successfully parsed Unicode XML database file!")
        return Result.Ok(unicode_xml)
    except Exception as ex:
        error = f"Error occurred parsing Unicode XML database file: {repr(ex)}"
        spinner.failed(error)
        return Result.Fail(error)


def parse_unicode_plane_and_block_data_from_xml(
    unicode_xml: _ElementTree, settings: UnicodeApiSettings
) -> Result[tuple[list[db.UnicodePlane], list[db.UnicodeBlock]]]:
    spinner = Spinner()
    spinner.start("Parsing Unicode plane and block data from XML database file...")
    all_planes = [db.UnicodePlane(**plane) for plane in json.loads(settings.PLANES_JSON.read_text())]
    result = parse_unicode_block_data_from_xml(unicode_xml, all_planes)
    if result.failure:
        return Result.Fail(result.error)
    if not result.value:
        return Result.Fail("Error parsing Unicode block data from XML database file: No data found!")
    all_blocks = result.value
    (all_planes, all_blocks) = get_block_range_for_each_plane(all_planes, all_blocks)
    spinner.successful("Successfully parsed Unicode plane and block data from XML database file!")
    return Result.Ok((all_planes, all_blocks))


def parse_unicode_block_data_from_xml(
    xml: _ElementTree, parsed_planes: list[db.UnicodePlane]
) -> Result[list[db.UnicodeBlock]]:
    all_blocks = xml.findall(".//block", {None: "http://www.unicode.org/ns/2003/ucd/1.0"})
    results = [parse_block_details(id, block, parsed_planes) for id, block in enumerate(all_blocks, start=1)]
    valid_results, invalid_results = evaluate_parse_results(results)
    if invalid_results:
        return Result.Fail(f"Error parsing Unicode block data from XML database file: {'\n\n'.join(invalid_results)}")
    return Result.Ok(valid_results)


def parse_block_details(id: int, block_node: _Element, parsed_planes: list[db.UnicodePlane]) -> Result[db.UnicodeBlock]:
    start = block_node.get("first-cp", "0")
    finish = block_node.get("last-cp", "0")
    start_dec = int(start, 16)
    finish_dec = int(finish, 16)
    plane = get_unicode_plane_containing_block_id(start_dec, finish_dec, parsed_planes)
    parsed_block = {
        "id": id,
        "long_name": block_node.get("name", ""),
        "short_name": "",
        "plane_id": plane.id or PROP_GROUP_INVALID_FOR_VERSION_ROW_ID,
        "start": f"{start_dec:04X}",
        "start_dec": start_dec,
        "finish": f"{finish_dec:04X}",
        "finish_dec": finish_dec,
        "total_allocated": finish_dec - start_dec + 1,
        "total_defined": 0,
    }
    return validate_parsed_unicode_data(parsed_block, db.UnicodeBlock)


def validate_parsed_unicode_data[T: UnicodeModel](parsed_data: dict[str, Any], db_model: type[T]) -> Result[T]:
    try:
        validated = db_model.model_validate(parsed_data)
        return Result.Ok(validated)
    except ValidationError as ex:
        return Result.Fail(create_validation_error_for_tui(ex, parsed_data))


def create_validation_error_for_tui(ex: ValidationError, parsed_data: dict[str, Any]) -> str:
    error_message = f"""\
    Parsed Unicode data is invalid:
    {get_section_header_for_tui("ERROR")}
    {repr(ex)}\n
    {get_section_header_for_tui("PARSED DATA")}
    {json.dumps(parsed_data, indent=4)}
    """
    return fill(dedent(error_message), width=ERROR_MESSAGE_MAX_WIDTH)


def get_section_header_for_tui(section_name: str, filler_char: str = "#") -> str:
    filler_char = filler_char[0]
    total_space_to_fill = ERROR_MESSAGE_MAX_WIDTH - len(f" {section_name} ")
    left_filler = right_filler = f"{filler_char}" * (total_space_to_fill // 2)
    if total_space_to_fill % 2:
        right_filler += filler_char
    return f"{left_filler} {section_name} {right_filler}"


def evaluate_parse_results[T: UnicodeModel](results: Sequence[Result[T]]) -> tuple[list[T], list[str]]:
    valid_results = [r.value for r in results if r.success and r.value]
    parse_errors = [r.error for r in results if r.failure]
    return (valid_results, parse_errors)


def get_unicode_plane_containing_block_id(
    start_dec: int, finish_dec: int, parsed_planes: list[db.UnicodePlane]
) -> db.UnicodePlane:
    found = [plane for plane in parsed_planes if plane.start_dec <= start_dec and finish_dec <= plane.finish_dec]
    return found[0] if found else NULL_PLANE


def get_block_range_for_each_plane(
    parsed_planes: list[db.UnicodePlane], parsed_blocks: list[db.UnicodeBlock]
) -> tuple[list[db.UnicodePlane], list[db.UnicodeBlock]]:
    for plane in parsed_planes:
        blocks_in_plane = [block for block in parsed_blocks if block.plane_id == plane.id]
        block_ids = sorted({block.id for block in blocks_in_plane if block and block.id is not None})
        if block_ids:
            plane.start_block_id = block_ids[0]
            plane.finish_block_id = block_ids[-1]
    return (parsed_planes, parsed_blocks)


def parse_unicode_character_data_from_xml(
    settings: UnicodeApiSettings,
    xml: _ElementTree,
    blocks: list[db.UnicodeBlock],
    planes: list[db.UnicodePlane],
) -> Result[tuple[list[db.UnicodeCharacter], list[db.UnicodeCharacter], list[db.UnicodeCharacterUnihan]]]:
    non_unihan_results: list[Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]] = []
    tangut_results: list[Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]] = []
    unihan_results: list[Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]] = []
    prop_value_id_map = json.loads(settings.PROP_VALUES_JSON.read_text())
    char_nodes = xml.findall(".//char", {None: "http://www.unicode.org/ns/2003/ucd/1.0"})
    spinner = Spinner()
    spinner.start("Parsing Unicode character data from XML database file...", total=len(char_nodes))
    for char in char_nodes:
        if "cp" not in char.keys():  # noqa: SIM118
            continue
        (unihan, tangut, result) = parse_character_details(prop_value_id_map, char, blocks, planes)
        if unihan:
            unihan_results.append(result)
        elif tangut:
            tangut_results.append(result)
        else:
            non_unihan_results.append(result)
        spinner.increment()
    spinner.successful("Successfully parsed Unicode character data from XML database file!")
    return validate_all_parsed_character_data(non_unihan_results, tangut_results, unihan_results)


def parse_character_details(
    prop_value_id_map: "UnicodePropertyGroupMap",
    char_node: _Element,
    parsed_blocks: list[db.UnicodeBlock],
    parsed_planes: list[db.UnicodePlane],
) -> tuple[bool, bool, Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]]:
    codepoint = char_node.get("cp", "0")
    codepoint_dec = int(codepoint, 16)
    block = get_unicode_block_containing_codepoint(codepoint_dec, parsed_blocks)
    plane = [plane for plane in parsed_planes if plane.id == block.plane_id][0]
    unihan = any(
        bname in block.long_name.lower() for bname in ["cjk unified ideographs", "cjk compatibility ideographs"]
    )
    tangut = "tangut" in block.long_name.lower()
    char: Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]

    char_props = {
        "codepoint_dec": codepoint_dec,
        "codepoint": codepoint,
        "name": get_character_name(char_node, codepoint, codepoint_dec, block),
        "bidi_mirrored": YES_NO_MAP[char_node.get("Bidi_M", "N")],
        "bidi_mirroring_glyph": get_mapped_codepoint(char_node.get("bmg", ""), codepoint),
        "bidi_control": YES_NO_MAP[char_node.get("Bidi_C", "N")],
        "bidi_paired_bracket_property": get_mapped_codepoint(char_node.get("bpb", ""), codepoint),
        "NFC_QC": db.TriadicLogic.from_code(char_node.get("NFC_QC", "")),
        "NFD_QC": db.TriadicLogic.from_code(char_node.get("NFD_QC", "")),
        "NFKC_QC": db.TriadicLogic.from_code(char_node.get("NFKC_QC", "")),
        "NFKD_QC": db.TriadicLogic.from_code(char_node.get("NFKD_QC", "")),
        "numeric_value": char_node.get("nv", ""),
        "joining_group": char_node.get("jg", ""),
        "join_control": YES_NO_MAP[char_node.get("Join_C", "N")],
        "uppercase": YES_NO_MAP[char_node.get("Upper", "N")],
        "lowercase": YES_NO_MAP[char_node.get("Lower", "N")],
        "simple_uppercase_mapping": get_mapped_codepoint(char_node.get("suc", ""), codepoint),
        "simple_lowercase_mapping": get_mapped_codepoint(char_node.get("slc", ""), codepoint),
        "simple_titlecase_mapping": get_mapped_codepoint(char_node.get("stc", ""), codepoint),
        "simple_case_folding": get_mapped_codepoint(char_node.get("scf", ""), codepoint),
        "script_extensions": char_node.get("scx", ""),
        "indic_syllabic_category": char_node.get("InSC", ""),
        "indic_matra_category": char_node.get("InMC", "") or "NA",
        "indic_positional_category": char_node.get("InPC", ""),
        "ideographic": YES_NO_MAP[char_node.get("Ideo", "N")],
        "unified_ideograph": YES_NO_MAP[char_node.get("UIdeo", "N")],
        "equivalent_unified_ideograph": char_node.get("EqUIdeo", ""),
        "radical": YES_NO_MAP[char_node.get("Radical", "N")],
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
        "regional_indicator": YES_NO_MAP[char_node.get("RI", "N")],
        "emoji": YES_NO_MAP[char_node.get("Emoji", "N")],
        "emoji_presentation": YES_NO_MAP[char_node.get("EPres", "N")],
        "emoji_modifier": YES_NO_MAP[char_node.get("EMod", "N")],
        "emoji_modifier_base": YES_NO_MAP[char_node.get("EBase", "N")],
        "emoji_component": YES_NO_MAP[char_node.get("EComp", "N")],
        "extended_pictographic": YES_NO_MAP[char_node.get("ExtPict", "N")],
        "block_id": block.id or 0,
        "plane_id": plane.id or -1,
        "general_category_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "General_Category", char_node.get("gc", "0")
        ),
        "age_id": get_prop_value_id_from_short_name(prop_value_id_map, "Age", char_node.get("age", "0")),
        "combining_class_id": get_prop_value_id_from_short_name(
            prop_value_id_map,
            "Canonical_Combining_Class",
            prop_value_id_map["Canonical_Combining_Class"][char_node.get("ccc", "0")]["short_name"],
            prop_value_id_map["Canonical_Combining_Class"]["0"]["id"],
        ),
        "bidi_class_id": get_prop_value_id_from_short_name(prop_value_id_map, "Bidi_Class", char_node.get("bc", "0")),
        "bidi_paired_bracket_type_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "Bidi_Paired_Bracket_Type", char_node.get("bpt", "")
        ),
        "decomposition_type_id": get_prop_value_id_from_short_name(
            prop_value_id_map,
            "Decomposition_Type",
            char_node.get("dt", ""),
            prop_value_id_map["Decomposition_Type"]["12"]["id"],
        ),
        "numeric_type_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "Numeric_Type", char_node.get("nt", "")
        ),
        "joining_type_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "Joining_Type", char_node.get("jt", "")
        ),
        "line_break_id": get_prop_value_id_from_short_name(prop_value_id_map, "Line_Break", char_node.get("lb", "")),
        "east_asian_width_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "East_Asian_Width", char_node.get("ea", "")
        ),
        "script_id": get_prop_value_id_from_short_name(prop_value_id_map, "Script", char_node.get("sc", "")),
        "hangul_syllable_type_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "Hangul_Syllable_Type", char_node.get("hst", "")
        ),
        "vertical_orientation_id": get_prop_value_id_from_short_name(
            prop_value_id_map, "Vertical_Orientation", char_node.get("vo", "")
        ),
    }

    if not unihan:
        char = validate_parsed_unicode_data(char_props, db.UnicodeCharacter)
    else:
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
        char_props.update(unihan_props)
        char = validate_parsed_unicode_data(char_props, db.UnicodeCharacterUnihan)
    return (unihan, tangut, char)


def get_prop_value_id_from_short_name(
    prop_value_id_map: "UnicodePropertyGroupMap", prop_group: str, short_name: str, default: int | None = None
) -> int:
    if (id_map := prop_value_id_map.get(prop_group)) and isinstance(id_map, dict):
        id_map_typed: dict[str, UnicodePropertyGroupValues] = id_map
        for prop_value in id_map_typed.values():
            if prop_value["short_name"].lower() == short_name.lower():
                return prop_value["id"]
        return default or 1
    return 999999


def get_unicode_block_containing_codepoint(codepoint: int, parsed_blocks: list[db.UnicodeBlock]) -> db.UnicodeBlock:
    found = [block for block in parsed_blocks if block.start_dec <= codepoint and codepoint <= block.finish_dec]
    return found[0] if found else NULL_BLOCK


def get_character_name(char_node: _Element, codepoint: str, codepoint_dec: int, block: db.UnicodeBlock) -> str:
    name = char_node.get("na", "")
    return (
        f"Undefined Codepoint ({get_codepoint_string(codepoint_dec)}) (Reserved for {block.long_name})"
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
    return f"<control-{codepoint:04X}>{control_char_names.get(codepoint, '')}"


def get_mapped_codepoint(prop_value: str, codepoint_hex: str) -> str:
    return codepoint_hex if prop_value == "#" else prop_value if prop_value else ""


def get_decomposition_mapping(decomposition_mapping: str, codepoint: int) -> str:
    return decomposition_mapping if decomposition_mapping != "#" else f"{codepoint:04X}"


def parse_numeric_value(numeric_value: str, codepoint: str) -> int | float | None:
    if not numeric_value or numeric_value == "NaN":
        return None
    try:
        if "/" in numeric_value:
            [num, denom] = numeric_value.split("/", maxsplit=1)
            return int(num.strip()) / float(denom.strip())
        return int(numeric_value.strip())
    except ValueError as ex:
        print(f"Error parsing numeric_value for codepoint {codepoint} (numeric_value={numeric_value}): {repr(ex)}")
        return None


def validate_all_parsed_character_data(
    non_unihan_results: list[Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]],
    tangut_results: list[Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]],
    unihan_results: list[Result[db.UnicodeCharacter | db.UnicodeCharacterUnihan]],
) -> Result[tuple[list[db.UnicodeCharacter], list[db.UnicodeCharacter], list[db.UnicodeCharacterUnihan]]]:
    all_parse_errors = []
    non_unihan_chars, non_unihan_parse_errors = evaluate_parse_results(non_unihan_results)
    if non_unihan_parse_errors:
        all_parse_errors.extend(non_unihan_parse_errors)
    tangut_chars, tangut_parse_errors = evaluate_parse_results(tangut_results)
    if tangut_parse_errors:
        all_parse_errors.extend(tangut_parse_errors)
    unihan_chars, unihan_parse_errors = evaluate_parse_results(unihan_results)
    if unihan_parse_errors:
        all_parse_errors.extend(unihan_parse_errors)
    if len(all_parse_errors) > 0:
        return Result.Fail(
            f"Error parsing Unicode character data from XML database file: {'\n\n'.join(all_parse_errors)}"
        )
    return Result.Ok((non_unihan_chars, tangut_chars, unihan_chars))


def finalize_all_parsed_unicode_data(
    settings: UnicodeApiSettings, all_parsed_data: AllParsedUnicodeData
) -> AllParsedUnicodeData:
    spinner = Spinner()
    spinner.start("Counting number of defined characters in each block and plane...")
    all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars = all_parsed_data
    update_block_property_values(settings, all_blocks)
    count_defined_characters_per_block(non_unihan_chars, tangut_chars, unihan_chars, all_blocks)
    count_defined_characters_per_plane(all_blocks, all_planes)
    spinner.successful("Successfully counted number of defined characters in each block and plane!")
    return (all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars)


def update_block_property_values(settings: UnicodeApiSettings, all_blocks: list[db.UnicodeBlock]):
    prop_value_id_map = json.loads(settings.PROP_VALUES_JSON.read_text())
    block_name_map = {normalize_string_lm3(block["long_name"]): block for block in prop_value_id_map["Block"].values()}
    updated_block_value_map = {}
    for block in all_blocks:
        prop_value_map = block_name_map.get(normalize_string_lm3(block.long_name), {})
        block.short_name = prop_value_map.get("short_name", block.long_name)
        updated_block_value_map[block.id] = {
            "id": block.id,
            "short_name": block.short_name,
            "long_name": block.long_name,
        }
    prop_value_id_map["Block"] = updated_block_value_map
    settings.PROP_VALUES_JSON.write_text(json.dumps(prop_value_id_map, indent=4))


def count_defined_characters_per_block(
    non_unihan_chars: list[db.UnicodeCharacter],
    tangut_chars: list[db.UnicodeCharacter],
    unihan_chars: list[db.UnicodeCharacterUnihan],
    all_blocks: list[db.UnicodeBlock],
):
    char_map = get_all_char_codepoint_map(non_unihan_chars, tangut_chars, unihan_chars)
    for block in all_blocks:
        block.total_allocated = block.finish_dec - block.start_dec + 1
        block.total_defined = count_defined_characters_in_range(char_map, block.start_dec, block.finish_dec)


def get_all_char_codepoint_map(
    non_unihan_chars: list[db.UnicodeCharacter],
    tangut_chars: list[db.UnicodeCharacter],
    unihan_chars: list[db.UnicodeCharacterUnihan],
) -> dict[int, CharUnicodeModel]:
    return {char.codepoint_dec: char for char in non_unihan_chars + tangut_chars + unihan_chars}


def count_defined_characters_in_range(char_map: dict[int, CharUnicodeModel], start: int, finish: int) -> int:
    return len([codepoint for codepoint in range(start, finish + 1) if codepoint in char_map])


def count_defined_characters_per_plane(all_blocks: list[db.UnicodeBlock], all_planes: list[db.UnicodePlane]):
    for plane in all_planes:
        plane.total_allocated = plane.finish_dec - plane.start_dec + 1
        plane.total_defined = sum(block.total_defined for block in all_blocks if block.plane_id == plane.id)
