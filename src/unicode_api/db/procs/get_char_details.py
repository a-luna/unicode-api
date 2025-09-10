from typing import TYPE_CHECKING, Any

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Mapped
from sqlmodel import col, select

import unicode_api.db.models as db
from unicode_api.core.cache import cached_data
from unicode_api.db.character_props import PROPERTY_GROUPS

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.db.models import CharPropertyGroup


def get_character_properties(
    engine: Engine, codepoint: int, show_props: list[db.CharPropertyGroup], verbose: bool
) -> dict[str, Any]:
    """
    Retrieve Unicode character properties for a specific codepoint.
    This function fetches various property groups for a Unicode character and
    returns them as a dictionary. The properties can be filtered by specific
    property groups and can include or exclude properties that are not relevant
    for the specific codepoint.

    Args:
        engine (Engine): SQLAlchemy engine instance for database access.

        codepoint (int): The Unicode codepoint value to retrieve properties for.

        show_props (list[db.CharPropertyGroup] | None): Optional list of property groups
            to include. If None, the default set of properties from the Minimum (or CJK
            Minimum) property group will be included.

        verbose (bool): If True, return all property values; if False, exclude
            properties that are not relevant for this codepoint.

    Returns:
        dict[str, Any]: A dictionary containing the character's properties.
            Keys are property names and values are the corresponding property values.
    """

    prop_groups = _get_prop_groups(codepoint, show_props)
    character_props = _get_prop_values(engine, codepoint, prop_groups)
    character_props = _trim_values_not_supported_in_this_version(character_props)
    return character_props if verbose else _trim_irrelevant_values(codepoint, character_props)


def _get_prop_groups(codepoint: int, show_props: list[db.CharPropertyGroup]) -> list[db.CharPropertyGroup]:
    unihan = cached_data.character_is_unihan(codepoint)
    props_set: set[CharPropertyGroup] = set(show_props) if show_props else set()
    # If all property groups are requested, return appropriate property groups for non-unihan/unihan
    if db.CharPropertyGroup.ALL in props_set:
        return (
            db.CharPropertyGroup.get_all_non_unihan_character_prop_groups()
            if not unihan
            else db.CharPropertyGroup.get_all_unihan_character_prop_groups()
        )
    # else, ensure that the Minimum property group appropriate for non-unihan/unihan is included
    props_set.add(db.CharPropertyGroup.MINIMUM if not unihan else db.CharPropertyGroup.CJK_MINIMUM)
    # if Basic property group is requested, ensure property group appropriate for non-unihan/unihan is included
    if unihan and db.CharPropertyGroup.BASIC in props_set:
        props_set.add(db.CharPropertyGroup.CJK_BASIC)
        props_set.remove(db.CharPropertyGroup.BASIC)
    # then, if character is non-unihan, ensure that any unihan-specific property groups are not included
    if not unihan:
        unihan_prop_groups = {prop_group for prop_group in db.CharPropertyGroup if "CJK" in prop_group.name}
        props_set = props_set.difference(unihan_prop_groups)

    return list(props_set)


def _get_prop_values(engine: Engine, codepoint: int, prop_groups: list[db.CharPropertyGroup]) -> dict[str, Any]:
    table = db.UnicodeCharacter if cached_data.character_is_non_unihan(codepoint) else db.UnicodeCharacterUnihan
    columns: list[Mapped[Any]] = []
    for prop_group in prop_groups:
        columns.extend([getattr(table, prop.name_in) for prop in PROPERTY_GROUPS[prop_group] if prop.db_column])
    char_props = _get_prop_values_from_database(engine, table, codepoint, columns)

    prop_values: dict[str, Any] = {}
    for prop_group in prop_groups:
        prop_values.update(
            {prop_map.name_out: prop_map.response_value(char_props) for prop_map in PROPERTY_GROUPS[prop_group]}
        )
    return prop_values


def _get_prop_values_from_database(
    engine: Engine,
    table: type[db.UnicodeCharacter | db.UnicodeCharacterUnihan],
    codepoint: int,
    columns: list[Mapped[Any]],
) -> dict[str, Any]:
    char_props = {"codepoint_dec": codepoint}
    if not columns:
        return char_props
    query = select(*columns).select_from(table).where(col(table.codepoint_dec) == codepoint)
    with engine.connect() as con:
        for row in con.execute(query).mappings():
            char_props.update(dict(row))
    return char_props


def _trim_values_not_supported_in_this_version(response_dict: dict[str, Any]) -> dict[str, Any]:  # pragma: no cover
    for prop_group_name in [pg for pg in cached_data.missing_property_groups if pg in response_dict]:
        response_dict.pop(prop_group_name)
    return response_dict


def _trim_irrelevant_values(codepoint: int, response_dict: dict[str, Any]) -> dict[str, Any]:
    for prop_name in _get_prop_names_with_irrelevant_values(codepoint, response_dict):
        response_dict.pop(prop_name)
    return response_dict


def _get_prop_names_with_irrelevant_values(codepoint: int, char_props: dict[str, Any]) -> list[str]:
    remove_props = (
        _get_unset_flag_properties(char_props)
        + _remove_irrelevant_casing_properties(char_props, codepoint)
        + _remove_irrelevant_indic_properties(char_props)
        + _get_all_other_properties_with_irrelevant_values(char_props, codepoint)
    )
    if cached_data.character_is_unihan(codepoint):
        remove_props.extend(_get_unihan_prop_names_with_null_values(char_props))
    return list(set(remove_props))


def _get_unihan_prop_names_with_null_values(char_props: dict[str, Any]) -> list[str]:
    unihan_list_properties = [
        "traditional_variant",
        "simplified_variant",
        "z_variant",
        "compatibility_variant",
        "semantic_variant",
        "specialized_semantic_variant",
        "spoofing_variant",
    ]
    remove_list_props = [
        prop_name for prop_name in unihan_list_properties if prop_name in char_props and char_props[prop_name] == [""]
    ]

    unihan_properties = [
        "ideo_frequency",
        "ideo_grade_level",
        "rs_count_unicode",
        "rs_count_kangxi",
        "total_strokes",
        "accounting_numeric",
        "primary_numeric",
        "other_numeric",
        "hangul",
        "cantonese",
        "mandarin",
        "japanese_kun",
        "japanese_on",
        "vietnamese",
    ]
    remove_props = [
        prop_name for prop_name in unihan_properties if prop_name in char_props and not char_props[prop_name]
    ]
    return remove_list_props + remove_props


def _get_unset_flag_properties(char_props: dict[str, Any]) -> list[str]:
    return [
        flag.db_column_name
        for flag in _get_removable_flag_properties(char_props)
        if flag.db_column_name in char_props and not char_props[flag.db_column_name]
    ]


def _get_removable_flag_properties(char_props: dict[str, Any]) -> list[db.CharacterFilterFlag]:
    removable_flags = list(db.CharacterFilterFlag)
    set_flag_props = [
        flag for flag in db.CharacterFilterFlag if flag.db_column_name in char_props and char_props[flag.db_column_name]
    ]
    if any(flag.is_emoji_flag for flag in set_flag_props):
        removable_flags = [flag for flag in db.CharacterFilterFlag if not flag.is_emoji_flag]
    return removable_flags


def _remove_irrelevant_casing_properties(char_props: dict[str, Any], codepoint: int) -> list[str]:
    remove_props: list[str] = []
    if "uppercase" in char_props and not char_props["uppercase"]:
        remove_props.append("uppercase")
    if "lowercase" in char_props and not char_props["lowercase"]:
        remove_props.append("lowercase")

    other_casing_props = [
        "simple_uppercase_mapping",
        "simple_lowercase_mapping",
        "simple_titlecase_mapping",
        "simple_case_folding",
    ]
    remove_props.extend(
        prop_name
        for prop_name in other_casing_props
        if prop_name in char_props
        and (
            char_props[prop_name] == cached_data.get_mapped_codepoint_from_int(codepoint) or char_props[prop_name] == ""
        )
    )
    return remove_props


def _remove_irrelevant_indic_properties(char_props: dict[str, Any]) -> list[str]:
    indic_properties = [
        "indic_syllabic_category",
        "indic_matra_category",
        "indic_positional_category",
    ]
    if (
        all(prop_name in char_props for prop_name in indic_properties)
        and "Other" in char_props["indic_syllabic_category"]
        and "NA" in char_props["indic_matra_category"]
        and "NA" in char_props["indic_positional_category"]
    ):
        return indic_properties
    return []


def _get_all_other_properties_with_irrelevant_values(char_props: dict[str, Any], codepoint: int) -> list[str]:
    remove_props: list[str] = []
    if "description" in char_props and not char_props["description"]:  # pragma: no cover
        remove_props.append("description")

    if "bidi_mirrored" in char_props and "bidi_mirroring_glyph" in char_props and not char_props["bidi_mirrored"]:
        remove_props.append("bidi_mirroring_glyph")

    if ("bidi_paired_bracket_type" in char_props and "None" in char_props["bidi_paired_bracket_type"]) and (
        "bidi_paired_bracket_property" in char_props
        and char_props["codepoint"] in char_props["bidi_paired_bracket_property"]
    ):
        remove_props.append("bidi_paired_bracket_type")
        remove_props.append("bidi_paired_bracket_property")

    if "decomposition_type" in char_props and "None" in char_props["decomposition_type"]:
        remove_props.append("decomposition_type")

    if "numeric_type" in char_props and "None" in char_props["numeric_type"]:
        remove_props.append("numeric_type")
        remove_props.append("numeric_value")
        remove_props.append("numeric_value_parsed")

    if "joining_type" in char_props and "Non_Joining" in char_props["joining_type"]:
        remove_props.append("joining_type")
        remove_props.append("joining_group")

    if "hangul_syllable_type" in char_props and "Not_Applicable" in char_props["hangul_syllable_type"]:
        remove_props.append("hangul_syllable_type")

    if "equivalent_unified_ideograph" in char_props and not char_props["equivalent_unified_ideograph"]:
        remove_props.append("equivalent_unified_ideograph")

    return remove_props
