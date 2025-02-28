import app.db.models as db
from app.core.cache import cached_data
from app.core.util import slugify
from app.enums.property_group import CharPropertyGroup

CHAR_TABLES = [db.UnicodeCharacter, db.UnicodeCharacterUnihan]


def create_table_listing_unicode_plane_abbreviations():
    html = """
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="plane-abbrev-values">
            <tbody>
                <tr>
                    <th>Abbreviation</th>
                    <th>Plane Name</th>
                </tr>"""
    for plane in cached_data.planes:
        html += f"""
                <tr>
                    <td>{plane.abbreviation}</td>
                    <td>{plane.name}</td>
                </tr>"""
    html += """
            </tbody>
        </table>
    </div>
</div>
"""
    return html


def create_table_listing_unicode_block_names(has_legend: bool = True):
    html = """          <div class="filter-table-outer">
                <div class="filter-table-wrapper">"""
    if has_legend:
        html += create_block_name_color_legend()
    html += """
                    <table id="block-name-values">
                        <thead>
                            <tr>
                                <th class="block-name-header"><strong>Block Range</strong></th>
                                <th class="block-name-header"><strong>Block Name</strong></th>
                                <th class="block-name-header"><strong>Short Name</strong></th>
                            </tr>
                        </thead>
                        <tbody>"""
    for block in cached_data.blocks:
        html += f"""
                            <tr>
                                <td><code>U+{block.start}...U+{block.finish}</code></td>
                                <td class="block-name" style="color: var(--{block.plane.abbreviation.lower()}-text-color)">{block.long_name.replace(" ", "_").replace("-", "_")}</td>"""
        if block.short_and_long_name_differ:
            html += f"""
                                <td class="block-short-name" style="color: var(--{block.plane.abbreviation.lower()}-text-color)">{block.short_name}</td>"""
        else:
            html += """
                                <td class="block-short-name" />"""
        html += """
                            </tr>"""
    html += """
                        </tbody>
                    </table>
                </div>
            </div>"""
    return html


def create_block_name_color_legend():
    html = """
                    <div class="block-name-info">
                        <p>The color of each block name indicates the plane it belongs to:</p>
                        <div class="block-name-color-legend-wrapper">
                            <ul class="block-name-color-legend">"""
    for plane in cached_data.planes[:4]:
        html += f"""
                                <li style="color: var(--{plane.abbreviation.lower()}-text-color)"><span class="color-swatch" style="background-color: var(--{plane.abbreviation.lower()}-text-color)"></span><span>{plane.name} ({plane.abbreviation})</span></li>"""
    html += """
                            </ul>
                            <ul class="block-name-color-legend">"""
    for plane in cached_data.planes[4:]:
        html += f"""
                                <li style="color: var(--{plane.abbreviation.lower()}-text-color)"><span class="color-swatch" style="background-color: var(--{plane.abbreviation.lower()}-text-color)"></span><span>{plane.name} ({plane.abbreviation})</span></li>"""
    html += """
                            </ul>
                        </div>
                    </div>"""
    return html


def create_table_listing_prop_group_names() -> str:
    html = """
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="prop-group-values">
            <tbody>
                <tr>
                    <th>Property Group</th>
                    <th>Alias</th>
                </tr>"""
    for pg in CharPropertyGroup:
        if pg not in [
            CharPropertyGroup.NONE,
            CharPropertyGroup.MINIMUM,
            CharPropertyGroup.CJK_MINIMUM,
            CharPropertyGroup.CJK_BASIC,
        ]:
            html += f"""
                    <tr>
                        <td>{get_prop_group_name_maybe_linked(pg)}</td>
                        <td>{pg.short_alias if pg.has_alias else ""}</td>
                    </tr>"""
    html += """
            </tbody>
        </table>
    </div>
</div>"""
    return html


def get_prop_group_name_maybe_linked(pg: CharPropertyGroup) -> str:
    return f'<a href="#{slugify(pg.name)}">{pg}</a>' if pg != CharPropertyGroup.ALL else str(pg)


def get_html_for_general_category_values_table() -> str:
    html = """
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="general-category-values">
            <tbody>
                <tr>
                    <th>Code</th>
                    <th>Category</th>
                </tr>"""
    for val in cached_data.get_all_values_for_property_group("General_Category"):
        if val.get("is_group"):
            html += f"""
                <tr class="group-category">
                    <td>{val["short_name"]}</td>
                    <td>{val.get("grouped_values", "")}</td>
                </tr>"""
        else:
            html += f"""
                <tr>
                    <td>{val["short_name"]}</td>
                    <td>{val["long_name"]}</td>
                </tr>"""
    html += """
            </tbody>
        </table>
    </div>
</div>"""
    return html


def get_html_for_property_group_values_table(
    group_name: str,
    filter_param: str,
    column_1_text: str = "Code",
    hide_column_2: bool = False,
    column_2_text: str = "Long Name",
) -> str:
    html = f"""
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="{filter_param}-values">
            <tbody>
                <tr>"""
    if filter_param == "ccc":
        html += """
                    <th>Category ID</th>"""
    html += f"""
                    <th>{column_1_text}</th>"""
    if not hide_column_2:
        html += f"""
                    <th>{column_2_text}</th>"""
    html += """
                </tr>"""
    for val in cached_data.get_all_values_for_property_group(group_name):
        html += """
                <tr>"""
        if filter_param == "ccc":
            html += f"""
                    <td>{val["id"]}</td>"""
        html += f"""
                    <td>{val["short_name"]}</td>"""
        if not hide_column_2:
            html += f"""
                    <td>{val["long_name"]}</td>"""
        html += """
                </tr>"""
    html += """
            </tbody>
        </table>
    </div>
</div>"""
    return html


def get_html_for_character_flags_table() -> str:
    html = """
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="flag-values">
            <tbody>
                <tr>
                    <th>Flags (Boolean Properties)</th>
                    <th>Short Name</th>"""
    html += """
                </tr>"""
    for flag in db.CharacterFilterFlag:
        html += f"""
                <tr>
                    <td>{flag.display_name}</td>
                    <td>{flag.db_column_name}</td>"""
        html += """
                </tr>"""
    html += """
            </tbody>
        </table>
    </div>
</div>"""
    return html


PLANE_ABBREV_VALUES_TABLE = create_table_listing_unicode_plane_abbreviations()
BLOCK_NAME_VALUES_TABLE = create_table_listing_unicode_block_names()
BLOCK_NAME_NO_LEGEND_TABLE = create_table_listing_unicode_block_names(has_legend=False)
PROPERTY_GROUP_VALUES_TABLE = create_table_listing_prop_group_names()
GENERAL_CATEGORY_VALUES_TABLE = get_html_for_general_category_values_table()
UNICODE_AGE_VALUES_TABLE = get_html_for_property_group_values_table(
    "Age", "age", column_1_text="Unicode Version", hide_column_2=True
)
SCRIPT_CODE_VALUES_TABLE = get_html_for_property_group_values_table("Script", "script", column_2_text="Script Name")
BIDI_CLASS_VALUES_TABLE = get_html_for_property_group_values_table(
    "Bidi_Class", "bidi_class", column_2_text="Bidirectional Class"
)
DECOMP_TYPE_VALUES_TABLE = get_html_for_property_group_values_table(
    "Decomposition_Type", "decomp_type", column_2_text="Decomposition Type"
)
LINE_BREAK_TYPE_VALUES_TABLE = get_html_for_property_group_values_table(
    "Line_Break", "line_break", column_2_text="Line Break Type"
)
CCC_VALUES_TABLE = get_html_for_property_group_values_table(
    "Canonical_Combining_Class", "ccc", column_2_text="Combining Class Category"
)
NUMERIC_TYPES_TABLE = get_html_for_property_group_values_table("Numeric_Type", "num_type", column_2_text="Numeric Type")
JOINING_TYPES_TABLE = get_html_for_property_group_values_table(
    "Joining_Type", "join_type", column_2_text="Joining Type"
)
CHAR_FLAGS_TABLE = get_html_for_character_flags_table()
