import re

from app.core.config import ROOT_FOLDER
from app.docs.api_docs.content.block import BLOCK_ENDPOINTS, UNICODE_BLOCK_OBJECT_INTRO, UNICODE_BLOCK_OBJECT_PROPERTIES
from app.docs.api_docs.content.character import (
    CHARACTER_ENDPOINTS,
    PROP_GROUP_BASIC,
    PROP_GROUP_BIDIRECTIONALITY,
    PROP_GROUP_CASE,
    PROP_GROUP_DECOMPOSITION,
    PROP_GROUP_EAW,
    PROP_GROUP_EMOJI,
    PROP_GROUP_F_AND_G,
    PROP_GROUP_HANGUL,
    PROP_GROUP_INDIC,
    PROP_GROUP_JOINING,
    PROP_GROUP_LINEBREAK,
    PROP_GROUP_MINIMUM,
    PROP_GROUP_NUMERIC,
    PROP_GROUP_QUICK_CHECK,
    PROP_GROUP_SCRIPT,
    PROP_GROUP_UTF8,
    PROP_GROUP_UTF16,
    PROP_GROUP_UTF32,
    UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1,
    UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2,
    UNICODE_CHARACTER_PROP_GROUPS_INTRO,
    UNICODE_CHATACTER_OBJECT_INTRO,
)
from app.docs.api_docs.content.intro import INTRODUCTION, LOOSE_MATCHING, PAGINATION, PROJECT_LINKS_README, SEARCH
from app.docs.api_docs.content.plane import PLANE_ENDPOINTS, UNICODE_PLANE_OBJECT_INTRO, UNICODE_PLANE_OBJECT_PROPERTIES
from app.docs.util import slugify

HtmlHeading = dict[str, int | str]
HeadingMap = dict[int, list[HtmlHeading]]

HEADING_ELEMENT_REGEX = re.compile(
    r'h(?P<level>2|3|4|5|6) id="(?P<slug>[0-9a-z-_]+)">(?P<text>.+)<\/(?:h2|h3|h4|h5|h6)>'
)


def create_details_element_readme(title: str, content: str, open: bool | None = False) -> str:
    open_tag = "<details open>" if open else "<details>"
    return f"""\t\t{open_tag}
            <summary>
                <strong>{title}</strong>
            </summary>{content}\t\t</details>
"""


def create_readme_section(heading_level: int, title: str, content: str):
    return f'<h{heading_level} id="{slugify(title)}">{title}</h{heading_level}>' + content


UNICODE_CHARACTER_PROP_GROUPS_README = (
    f'{create_details_element_readme("<strong>Minimum</strong>", PROP_GROUP_MINIMUM, True)}'
    + "\t\t<br />\n"
    + UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1
    + "\t\t"
    + UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2
    + f'{create_details_element_readme("<strong>Basic</strong>", PROP_GROUP_BASIC)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>UTF-8</strong>", PROP_GROUP_UTF8)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>UTF-16</strong>", PROP_GROUP_UTF16)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>UTF-32</strong>", PROP_GROUP_UTF32)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Bidirectionality</strong>", PROP_GROUP_BIDIRECTIONALITY)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Decomposition</strong>", PROP_GROUP_DECOMPOSITION)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Quick Check</strong>", PROP_GROUP_QUICK_CHECK)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Numeric</strong>", PROP_GROUP_NUMERIC)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Joining</strong>", PROP_GROUP_JOINING)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Linebreak</strong>", PROP_GROUP_LINEBREAK)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>East Asian Width</strong>", PROP_GROUP_EAW)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Case</strong>", PROP_GROUP_CASE)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Script</strong>", PROP_GROUP_SCRIPT)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Hangul</strong>", PROP_GROUP_HANGUL)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Indic</strong>", PROP_GROUP_INDIC)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Function and Graphic</strong>", PROP_GROUP_F_AND_G)}'
    + "\t\t<br />\n"
    + f'{create_details_element_readme("<strong>Emoji</strong>", PROP_GROUP_EMOJI)}'
)

UNICODE_CHARACTERS_DOCS = f"""
    <div>
{create_details_element_readme('<h4 id="character-api-endpoints">API Endpoints</h4>', CHARACTER_ENDPOINTS, True)}\t\t<h4 id="the-unicodecharacter-object">The <code>UnicodeCharacter</code> Object</h4>
        {UNICODE_CHATACTER_OBJECT_INTRO}
        <h4 id="unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</h4>
        {UNICODE_CHARACTER_PROP_GROUPS_INTRO}
{UNICODE_CHARACTER_PROP_GROUPS_README}\t</div>
"""

UNICODE_BLOCKS_DOCS = f"""
    <div>
        {create_details_element_readme('<h4 id="block-api-endpoints">API Endpoints</h4>', BLOCK_ENDPOINTS, True)}\t\t<h4 id="the-unicodeblock-object">The <code>UnicodeBlock</code> Object</h4>
        {UNICODE_BLOCK_OBJECT_INTRO}
{create_details_element_readme("<strong><code>UnicodeBlock</code> Properties</strong>", UNICODE_BLOCK_OBJECT_PROPERTIES)}\t</div>
"""

UNICODE_PLANES_DOCS = f"""
    <div>
        {create_details_element_readme('<h4 id="plane-api-endpoints">API Endpoints</h4>', PLANE_ENDPOINTS, True)}\t\t<h4 id="the-unicodeplane-object">The <code>UnicodePlane</code> Object</h4>
        {UNICODE_PLANE_OBJECT_INTRO}
{create_details_element_readme("<strong><code>UnicodePlane</code> Properties</strong>", UNICODE_PLANE_OBJECT_PROPERTIES)}\t</div>
"""


def update_readme():
    readme_api_docs = f"<h1>Unicode API</h1>\n{create_toc_for_readme()}{get_api_docs_for_readme()}"
    ROOT_FOLDER.joinpath("README.md").write_text(readme_api_docs)


def create_toc_for_readme():
    html = get_api_docs_for_readme()
    toc = create_toc_section(2, 0, len(html), create_html_heading_map(html))
    html = '<ul class="toc">\n'
    for section in toc:
        html += create_toc_section_html(section, 0)
    html += "</ul>\n"
    return html


def get_api_docs_for_readme():
    return (
        create_readme_section(2, "Introduction", INTRODUCTION)
        + create_readme_section(2, "Project Resources/Contact Info", PROJECT_LINKS_README)
        + create_readme_section(2, "Pagination", PAGINATION)
        + create_readme_section(2, "Search", SEARCH)
        + create_readme_section(2, "Loose Matching", LOOSE_MATCHING)
        + '<h2 id="core-resources">Core Resources</h2>\n'
        + create_readme_section(3, "Unicode Characters", UNICODE_CHARACTERS_DOCS)
        + create_readme_section(3, "Unicode Blocks", UNICODE_BLOCKS_DOCS)
        + create_readme_section(3, "Unicode Planes", UNICODE_PLANES_DOCS)
    )


def create_html_heading_map(html) -> HeadingMap:
    heading_elements = []
    for match in HEADING_ELEMENT_REGEX.finditer(html):
        match_dict = match.groupdict()
        heading_elements.append(
            {
                "level": int(match_dict["level"]),
                "slug": match_dict["slug"],
                "text": match_dict["text"],
                "index": match.start(),
            }
        )
    return {
        heading_level: [h for h in heading_elements if h["level"] == heading_level] for heading_level in range(2, 7)
    }


def create_toc_section(level: int, section_start: int, section_end: int, heading_map: HeadingMap):
    level_map = [h for h in heading_map[level] if (int(h["index"]) >= section_start and section_end > int(h["index"]))]
    if not level_map or not len(level_map):
        return []
    toc = []
    for i, heading in enumerate(level_map):
        if i < len(level_map) - 1:
            end = (int(level_map[i + 1]["index"]) or 0) - 1
        else:
            end = section_end
        toc.append(
            {"heading": heading, "children": create_toc_section(level + 1, int(heading["index"]), end, heading_map)}
        )
    return toc


def create_toc_section_html(section, indent_count):
    html = ("\t" * (indent_count + 1)) + "<li>\n"
    html += ("\t" * (indent_count + 2)) + f'<a href="#{section["heading"]["slug"]}">{section["heading"]["text"]}</a>\n'
    if section["children"]:
        html += ("\t" * (indent_count + 2)) + "<ul>\n"
        for sub_toc in section["children"]:
            html += create_toc_section_html(sub_toc, indent_count + 2)
        html += ("\t" * (indent_count + 2)) + "</ul>\n"
    html += ("\t" * (indent_count + 1)) + "</li>\n"
    return html
