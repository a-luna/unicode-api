from app.data.cache import cached_data
from app.docs.api_docs.swagger_ui import create_details_element_for_swagger_ui
from app.docs.util import slugify
from app.schemas.enums import BidirectionalClass, CharPropertyGroup, ScriptCode, UnicodeAge

GENERAL_CATEGORY_VALUES = """
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


def create_unicode_block_name_details_element():
    dt_elements = [f"\t\t\t\t<dt><code>U+{b.start}...U+{b.finish}</code></dt>\n" for b in cached_data.blocks]
    dd_elements = [
        (
            '\t\t\t\t<dd class="block-name" '
            f'style="color: var(--{b.plane.abbreviation.lower()}-text-color)">'
            f"{b.name}</dd>\n"
        )
        for b in cached_data.blocks
    ]
    block_data = zip(dt_elements, dd_elements, strict=True)
    html = '\t\t\t<div class="filter-table-outer">\n'
    html += '\t\t\t\t<div class="filter-table-wrapper">\n'
    html += create_block_name_color_legend()
    html += "\t\t\t\t\t<dl>\n"
    html += '\t\t\t\t\t\t<dt class="block-name-header"><strong>Block Range</strong></dt>\n'
    html += '\t\t\t\t\t\t<dd class="block-name-header"><strong>Block Name</strong></dd>\n'
    for dt, dd in block_data:
        html += dt
        html += dd
    html += "\t\t\t\t\t</dl>\n"
    html += "\t\t\t\t</div>\n"
    html += "\t\t\t</div>\n"
    return html


def create_block_name_color_legend():
    list_items = [
        (
            f'\t\t\t\t\t<li style="color: var(--{p.abbreviation.lower()}-text-color)">'
            f'<span class="color-swatch" style="background-color: var(--{p.abbreviation.lower()}-text-color)"></span>'
            f"<span>{p.name} ({p.abbreviation})</span></li>\n"
        )
        for p in cached_data.planes
    ]
    col_1 = list_items[:4]
    col_2 = list_items[4:]
    html = '\t\t\t<div class="block-name-info">\n'
    html += "\t\t\t\t<p>The color of each block name indicates the plane it belongs to:</p>\n"
    html += '\t\t\t\t<div class="block-name-color-legend-wrapper">\n'
    html += '\t\t\t\t\t<ul class="block-name-color-legend">\n'
    for el in col_1:
        html += el
    html += "\t\t\t\t\t</ul>\n"
    html += '\t\t\t\t\t<ul class="block-name-color-legend">\n'
    for el in col_2:
        html += el
    html += "\t\t\t\t\t</ul>\n"
    html += "\t\t\t\t</div>\n"
    html += "\t\t\t</div>\n"
    return html


def create_table_listing_unicode_age_values() -> str:
    html = """<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="unicode-age-values">
            <tbody>
                <tr>
                    <th>Unicode Version</th>
                </tr>
        """
    for age in UnicodeAge:
        html += f"""\t\t\t\t<tr>
                    <td>{age}</td>
                </tr>
            """
    html += """\t\t\t</tbody>
        </table>
    </div>
</div>
    """
    return html


def create_table_listing_prop_group_names() -> str:
    html = """<div class="filter-table-outer">
    <div class="filter-table-wrapper">
        <table id="prop-group-values">
            <tbody>
                <tr>
                    <th>Property Group</th>
                    <th>Alias</th>
                </tr>
    """
    for pg in CharPropertyGroup:
        html += f"""\t\t\t\t<tr>
                    <td>{get_prop_group_name_maybe_linked(pg)}</td>
                    <td>{pg.short_alias if pg.has_alias else ""}</td>
                </tr>
            """
    html += """\t\t\t</tbody>
        </table>
    </div>
</div>
    """
    return html


def get_prop_group_name_maybe_linked(pg: CharPropertyGroup) -> str:
    return f'<a href="#{slugify(pg.name)}">{pg.name}</a>' if pg != CharPropertyGroup.All else pg.name


def create_table_listing_enum_values(
    enumClass, filter_param, column_1_text="Code", column_2_text="Description", hide_column_2=False
) -> str:
    html = f"""<div class="filter-table-outer">
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
        if e.code:
            html += f"""
                <tr>
                    <td>{e.code}</td>"""
            if not hide_column_2:
                html += f"""
                    <td>{e}</td>"""
        html += """
                </tr>"""
    html += """
            </tbody>
        </table>
    </div>
</div>"""
    return html


BLOCK_NAME_VALUES_TABLE = create_details_element_for_swagger_ui(
    "Unicode Block Names", create_unicode_block_name_details_element()
)

GENERAL_CATEGORY_VALUES_TABLE = GENERAL_CATEGORY_VALUES
UNICODE_AGE_VALUES_TABLE = create_table_listing_unicode_age_values()
PROPERTY_GROUP_VALUES_TABLE = create_table_listing_prop_group_names()
SCRIPT_CODE_VALUES_TABLE = create_table_listing_enum_values(ScriptCode, "script-code", column_2_text="Script Name")
BIDI_CLASS_VALUES_TABLE = create_table_listing_enum_values(
    BidirectionalClass, "bidi-class", column_2_text="Bidirectional Class"
)
