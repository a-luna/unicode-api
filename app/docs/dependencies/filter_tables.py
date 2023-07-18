from app.data.cache import cached_data
from app.docs.util import slugify
from app.schemas.enums import (
    BidirectionalClass,
    CharacterFilterFlags,
    CharPropertyGroup,
    CombiningClassCategory,
    DecompositionType,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
)
from app.schemas.enums.unicode_age import UnicodeAge

GENERAL_CATEGORY_VALUES_TABLE = """
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="general-category-values">
            <tbody>
                <tr>
                    <th>Code</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>Lu</td>
                    <td>an uppercase letter</td>
                </tr>
                <tr>
                    <td>Ll</td>
                    <td>a lowercase letter</td>
                </tr>
                <tr>
                    <td>Lt</td>
                    <td>a digraphic character, with first part uppercase</td>
                </tr>
                <tr class="group-category">
                    <td>LC</td>
                    <td>Lu | Ll | Lt</td>
                </tr>
                <tr>
                    <td>Lm</td>
                    <td>a modifier letter</td>
                </tr>
                <tr>
                    <td>Lo</td>
                    <td>other letters, including syllables and ideographs</td>
                </tr>
                <tr class="group-category">
                    <td>L</td>
                    <td>Lu | Ll | Lt | Lm | Lo</td>
                </tr>
                <tr>
                    <td>Mn</td>
                    <td>a nonspacing combining mark (zero advance width)</td>
                </tr>
                <tr>
                    <td>Mc</td>
                    <td>a spacing combining mark (positive advance width)</td>
                </tr>
                <tr>
                    <td>Me</td>
                    <td>an enclosing combining mark</td>
                </tr>
                <tr class="group-category">
                    <td>M</td>
                    <td>Mn | Mc | Me</td>
                </tr>
                <tr>
                    <td>Nd</td>
                    <td>a decimal digit</td>
                </tr>
                <tr>
                    <td>Nl</td>
                    <td>a letterlike numeric character</td>
                </tr>
                <tr>
                    <td>No</td>
                    <td>a numeric character of other type</td>
                </tr>
                <tr class="group-category">
                    <td>N</td>
                    <td>Nd | Nl | No</td>
                </tr>
                <tr>
                    <td>Pc</td>
                    <td>a connecting punctuation mark, like a tie</td>
                </tr>
                <tr>
                    <td>Pd</td>
                    <td>a dash or hyphen punctuation mark</td>
                </tr>
                <tr>
                    <td>Ps</td>
                    <td>an opening punctuation mark (of a pair)</td>
                </tr>
                <tr>
                    <td>Pe</td>
                    <td>a closing punctuation mark (of a pair)</td>
                </tr>
                <tr>
                    <td>Pi</td>
                    <td>an initial quotation mark</td>
                </tr>
                <tr>
                    <td>Pf</td>
                    <td>a final quotation mark</td>
                </tr>
                <tr>
                    <td>Po</td>
                    <td>a punctuation mark of other type</td>
                </tr>
                <tr class="group-category">
                    <td>P</td>
                    <td>Pc | Pd | Ps | Pe | Pi | Pf | Po</td>
                </tr>
                <tr>
                    <td>Sm</td>
                    <td>a symbol of mathematical use</td>
                </tr>
                <tr>
                    <td>Sc</td>
                    <td>a currency sign</td>
                </tr>
                <tr>
                    <td>Sk</td>
                    <td>a non-letterlike modifier symbol</td>
                </tr>
                <tr>
                    <td>So</td>
                    <td>a symbol of other type</td>
                </tr>
                <tr class="group-category">
                    <td>S</td>
                    <td>Sm | Sc | Sk | So</td>
                </tr>
                <tr>
                    <td>Zs</td>
                    <td>a space character (of various non-zero widths)</td>
                </tr>
                <tr>
                    <td>Zl</td>
                    <td><code>U+2028 <span>LINE SEPARATOR</span></code> only</td>
                </tr>
                <tr>
                    <td>Zp</td>
                    <td><code>U+2029 <span>PARAGRAPH SEPARATOR</span></code> only</td>
                </tr>
                <tr class="group-category">
                    <td>Z</td>
                    <td>Zs | Zl | Zp</td>
                </tr>
                <tr>
                    <td>Cc</td>
                    <td>a <code>C0</code> or <code>C1</code> control code</td>
                </tr>
                <tr>
                    <td>Cf</td>
                    <td>a format control character</td>
                </tr>
                <tr>
                    <td>Cs</td>
                    <td>a surrogate code point</td>
                </tr>
                <tr>
                    <td>Co</td>
                    <td>a private-use character</td>
                </tr>
                <tr>
                    <td>Cn</td>
                    <td>a reserved unassigned code point or a noncharacter</td>
                </tr>
                <tr class="group-category">
                    <td>C</td>
                    <td>Cc | Cf | Cs | Co | Cn</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
"""


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
                            </tr>
                        </thead>
                        <tbody>"""
    for block in cached_data.blocks:
        html += f"""
                            <tr>
                                <td><code>U+{block.start}...U+{block.finish}</code></td>
                                <td class="block-name" style="color: var(--{block.plane.abbreviation.lower()}-text-color)">{block.name.replace(" ", "_").replace("-", "_")}</td>
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


def create_table_listing_enum_values(
    enumClass,
    filter_param,
    column_1_text="Code",
    column_1_attr="code",
    hide_column_2=False,
    column_2_text="Description",
    column_2_attr=None,
) -> str:
    html = f"""
<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="{filter_param}-values">
            <tbody>
                <tr>
                    <th>{column_1_text}</th>"""
    if not hide_column_2:
        html += f"""
                    <th>{column_2_text}</th>"""
    html += """
                </tr>"""
    for e in enumClass:
        if e.name != "NONE" and str(e) != "NONE" and hasattr(e, column_1_attr):
            html += f"""
                <tr>
                    <td>{getattr(e, column_1_attr)}</td>"""
            if not hide_column_2:
                col_2_value = getattr(e, column_2_attr, str(e)) if column_2_attr else str(e)
                html += f"""
                    <td>{col_2_value}</td>"""
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
UNICODE_AGE_VALUES_TABLE = create_table_listing_enum_values(
    UnicodeAge, "age", "Unicode Version Number", "value", hide_column_2=True
)
SCRIPT_CODE_VALUES_TABLE = create_table_listing_enum_values(ScriptCode, "script", column_2_text="Script Name")
BIDI_CLASS_VALUES_TABLE = create_table_listing_enum_values(
    BidirectionalClass, "bidi_class", column_2_text="Bidirectional Class"
)
DECOMP_TYPE_VALUES_TABLE = create_table_listing_enum_values(
    DecompositionType, "decomp_type", column_2_text="Decomposition Type"
)
LINE_BREAK_TYPE_VALUES_TABLE = create_table_listing_enum_values(
    LineBreakType, "line_break", column_2_text="Line Break Type"
)
CCC_VALUES_TABLE = create_table_listing_enum_values(
    CombiningClassCategory, "ccc", column_2_text="Combining Class Category"
)
NUMERIC_TYPES_TABLE = create_table_listing_enum_values(NumericType, "num_type", column_2_text="Numeric Type")
JOINING_TYPES_TABLE = create_table_listing_enum_values(JoiningType, "join_type", column_2_text="Joining Type")
CHAR_FLAGS_TABLE = create_table_listing_enum_values(
    CharacterFilterFlags,
    "flag",
    column_1_text="Flags (Boolean Properties)",
    column_1_attr="display_name",
    column_2_text="Alias",
    column_2_attr="short_alias",
)
