from __future__ import annotations

import re
from dataclasses import dataclass

from app.config.api_settings import get_settings
from app.core.result import Result
from app.docs.api_docs.content.block import BLOCK_ENDPOINTS, UNICODE_BLOCK_OBJECT_INTRO, UNICODE_BLOCK_OBJECT_PROPERTIES
from app.docs.api_docs.content.character import (
    CHARACTER_ENDPOINTS,
    CHARACTER_OBJECT_INTRO,
    CHARACTER_PROP_GROUPS_CONTINUED_1,
    CHARACTER_PROP_GROUPS_CONTINUED_2,
    CHARACTER_PROP_GROUPS_INTRO,
    PROP_GROUP_BASIC,
    PROP_GROUP_BIDIRECTIONALITY,
    PROP_GROUP_CASE,
    PROP_GROUP_CJK_NUMERIC,
    PROP_GROUP_CJK_READINGS,
    PROP_GROUP_CJK_VARIANTS,
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
    VERBOSITY,
)
from app.docs.api_docs.content.codepoint import CODEPOINT_CONTENT, CODEPOINTS_ENDPOINTS
from app.docs.api_docs.content.intro import (
    INTRODUCTION,
    LOOSE_MATCHING_HTML,
    PAGINATION_HTML,
    PROJECT_LINKS_README,
    SEARCH_HTML,
)
from app.docs.api_docs.content.plane import PLANE_ENDPOINTS, UNICODE_PLANE_OBJECT_INTRO, UNICODE_PLANE_OBJECT_PROPERTIES
from app.docs.util import slugify


@dataclass
class HtmlHeading:
    level: int
    slug: str
    text: str
    index: int


HeadingMap = dict[int, list[HtmlHeading]]


@dataclass
class TocSection:
    heading: HtmlHeading
    children: list[TocSection]


HEADING_ELEMENT_REGEX = re.compile(
    r'h(?P<level>2|3|4|5|6) id="(?P<slug>[0-9a-z-_]+)">(?P<text>.+)<\/(?:h2|h3|h4|h5|h6)>'
)


def create_details_element_readme(
    title: str, content: str, class_name: str | None = None, open: bool | None = False
) -> str:
    open_tag = "<details open" if open else "<details"
    open_tag += f" class={class_name!r}>" if class_name else ">"
    return f"""\t{open_tag}
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1">{title}</strong>
        </summary>{content}\t</details>
"""


def create_readme_section(title: str, content: str, heading_level: int):
    return f'<h{heading_level} id="{slugify(title)}">{title}</h{heading_level}>' + content


def create_details_element_for_api_endpoints(id: str, content: str, open: bool | None = False) -> str:
    title = f'<h4 id="{id}">API Endpoints</h4>'
    return create_details_element_readme(title=title, content=content, class_name="api-endpoints", open=open)


def create_details_element_for_property_group(prop_group: str, content: str, open: bool | None = False) -> str:
    title = f"<strong>{prop_group}</strong>"
    return create_details_element_readme(title=title, content=content, class_name="property-group", open=open)


# API ENDPOINT DETAILS ELEMENTS
CHARACTER_API_ENDPOINTS = create_details_element_for_api_endpoints(
    id="character-api-endpoints", content=CHARACTER_ENDPOINTS, open=True
)
CODEPOINT_API_ENDPOINTS = create_details_element_for_api_endpoints(
    id="codepoint-api-endpoints", content=CODEPOINTS_ENDPOINTS, open=True
)
BLOCK_API_ENDPOINTS = create_details_element_for_api_endpoints(
    id="block-api-endpoints", content=BLOCK_ENDPOINTS, open=True
)
PLANE_API_ENDPOINTS = create_details_element_for_api_endpoints(
    id="plane-api-endpoints", content=PLANE_ENDPOINTS, open=True
)

# CHARACTER PROPERTY GROUP DETAILS ELEMENTS
CHARACTER_PROP_GROUP_MINIMUM = create_details_element_for_property_group(
    prop_group="Minimum", content=PROP_GROUP_MINIMUM, open=True
)
CHARACTER_PROP_GROUP_BASIC = create_details_element_for_property_group(
    prop_group="Basic", content=PROP_GROUP_BASIC, open=False
)
CHARACTER_PROP_GROUP_UTF8 = create_details_element_for_property_group(
    prop_group="UTF-8", content=PROP_GROUP_UTF8, open=False
)
CHARACTER_PROP_GROUP_UTF16 = create_details_element_for_property_group(
    prop_group="UTF-16", content=PROP_GROUP_UTF16, open=False
)
CHARACTER_PROP_GROUP_UTF32 = create_details_element_for_property_group(
    prop_group="UTF-32", content=PROP_GROUP_UTF32, open=False
)
CHARACTER_PROP_GROUP_BIDIRECTIONALITY = create_details_element_for_property_group(
    prop_group="Bidirectionality", content=PROP_GROUP_BIDIRECTIONALITY, open=False
)
CHARACTER_PROP_GROUP_DECOMPOSITION = create_details_element_for_property_group(
    prop_group="Decomposition", content=PROP_GROUP_DECOMPOSITION, open=False
)
CHARACTER_PROP_GROUP_QUICK_CHECK = create_details_element_for_property_group(
    prop_group="Quick Check", content=PROP_GROUP_QUICK_CHECK, open=False
)
CHARACTER_PROP_GROUP_NUMERIC = create_details_element_for_property_group(
    prop_group="Numeric", content=PROP_GROUP_NUMERIC, open=False
)
CHARACTER_PROP_GROUP_JOINING = create_details_element_for_property_group(
    prop_group="Joining", content=PROP_GROUP_JOINING, open=False
)
CHARACTER_PROP_GROUP_LINEBREAK = create_details_element_for_property_group(
    prop_group="Linebreak", content=PROP_GROUP_LINEBREAK, open=False
)
CHARACTER_PROP_GROUP_EAW = create_details_element_for_property_group(
    prop_group="East Asian Width", content=PROP_GROUP_EAW, open=False
)
CHARACTER_PROP_GROUP_CASE = create_details_element_for_property_group(
    prop_group="Case", content=PROP_GROUP_CASE, open=False
)
CHARACTER_PROP_GROUP_SCRIPT = create_details_element_for_property_group(
    prop_group="Script", content=PROP_GROUP_SCRIPT, open=False
)
CHARACTER_PROP_GROUP_HANGUL = create_details_element_for_property_group(
    prop_group="Hangul", content=PROP_GROUP_HANGUL, open=False
)
CHARACTER_PROP_GROUP_INDIC = create_details_element_for_property_group(
    prop_group="Indic", content=PROP_GROUP_INDIC, open=False
)
CHARACTER_PROP_GROUP_CJK_VARIANTS = create_details_element_for_property_group(
    prop_group="CJK Variants", content=PROP_GROUP_CJK_VARIANTS, open=False
)
CHARACTER_PROP_GROUP_CJK_NUMERIC = create_details_element_for_property_group(
    prop_group="CJK Numeric", content=PROP_GROUP_CJK_NUMERIC, open=False
)
CHARACTER_PROP_GROUP_CJK_READINGS = create_details_element_for_property_group(
    prop_group="CJK Readings", content=PROP_GROUP_CJK_READINGS, open=False
)
CHARACTER_PROP_GROUP_F_AND_G = create_details_element_for_property_group(
    prop_group="Function and Graphic", content=PROP_GROUP_F_AND_G, open=False
)
CHARACTER_PROP_GROUP_EMOJI = create_details_element_for_property_group(
    prop_group="Emoji", content=PROP_GROUP_EMOJI, open=False
)


UNICODE_CHARACTER_PROP_GROUPS_README = (
    f"{CHARACTER_PROP_GROUP_MINIMUM}"
    + "\t<br />\n"
    + "\t"
    + CHARACTER_PROP_GROUPS_CONTINUED_1
    + "\t"
    + CHARACTER_PROP_GROUPS_CONTINUED_2
    + '\n\t<h4 id="verbosity">Verbosity</h4>\n'
    + f"\t{VERBOSITY}\n"
    + f"{CHARACTER_PROP_GROUP_BASIC}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_UTF8}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_UTF16}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_UTF32}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_BIDIRECTIONALITY}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_DECOMPOSITION}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_QUICK_CHECK}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_NUMERIC}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_JOINING}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_LINEBREAK}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_EAW}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_CASE}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_SCRIPT}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_HANGUL}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_INDIC}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_CJK_VARIANTS}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_CJK_NUMERIC}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_CJK_READINGS}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_F_AND_G}"
    + "\t<br />\n"
    + f"{CHARACTER_PROP_GROUP_EMOJI}"
)

# UNICODE CHARACTERS DOCS
UNICODE_CHARACTERS_DOCS = f"""
<div>
{CHARACTER_API_ENDPOINTS}\t<h4 id="the-unicodecharacter-object">The <code>UnicodeCharacter</code> Object</h4>
    {CHARACTER_OBJECT_INTRO}
    <h4 id="unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</h4>
    {CHARACTER_PROP_GROUPS_INTRO}
{UNICODE_CHARACTER_PROP_GROUPS_README}</div>
"""

# UNICODE CODEPOINTS DOCS
UNICODE_CODEPOINTS_DOCS = f"""
<div>
{CODEPOINT_API_ENDPOINTS}\t{CODEPOINT_CONTENT}
</div>
"""

# UNICODE BLOCKS DOCS
UNICODE_BLOCKS_DOCS = f"""
<div>
{BLOCK_API_ENDPOINTS}\t<h4 id="the-unicodeblock-object">The <code>UnicodeBlock</code> Object</h4>
    {UNICODE_BLOCK_OBJECT_INTRO}
{create_details_element_readme("<strong><code>UnicodeBlock</code> Properties</strong>", UNICODE_BLOCK_OBJECT_PROPERTIES)}</div>
"""

# UNICODE PLANES DOCS
UNICODE_PLANES_DOCS = f"""
<div>
{PLANE_API_ENDPOINTS}\t<h4 id="the-unicodeplane-object">The <code>UnicodePlane</code> Object</h4>
    {UNICODE_PLANE_OBJECT_INTRO}
{create_details_element_readme("<strong><code>UnicodePlane</code> Properties</strong>", UNICODE_PLANE_OBJECT_PROPERTIES)}</div>
"""


def update_readme():
    html = get_api_docs_for_readme()
    readme_api_docs = f"<h1>Unicode API</h1>\n{create_toc_for_html(html)}{html}"
    get_settings().ROOT_FOLDER.joinpath("README.md").write_text(readme_api_docs)
    return Result.Ok()


def get_api_docs_for_readme():
    return (
        create_readme_section("Introduction", content=INTRODUCTION, heading_level=2)
        + create_readme_section("Project Resources/Contact Info", content=PROJECT_LINKS_README, heading_level=2)
        + create_readme_section("Pagination", content=PAGINATION_HTML, heading_level=2)
        + create_readme_section("Search", content=SEARCH_HTML, heading_level=2)
        + create_readme_section("Loose Matching", content=LOOSE_MATCHING_HTML, heading_level=2)
        + '<h2 id="core-resources">Core Resources</h2>\n'
        + create_readme_section("Unicode Characters", content=UNICODE_CHARACTERS_DOCS, heading_level=3)
        + create_readme_section("Unicode Codepoints", content=UNICODE_CODEPOINTS_DOCS, heading_level=3)
        + create_readme_section("Unicode Blocks", content=UNICODE_BLOCKS_DOCS, heading_level=3)
        + create_readme_section("Unicode Planes", content=UNICODE_PLANES_DOCS, heading_level=3)
    )


def create_toc_for_html(html: str) -> str:
    toc = create_toc_section(level=2, start=0, end=len(html), heading_map=create_html_heading_map(html))
    html = '<ul class="toc">\n'
    for section in toc:
        html += create_toc_section_html(section)
    html += "</ul>\n"
    return html


def create_html_heading_map(html: str) -> HeadingMap:
    heading_elements = [
        HtmlHeading(
            level=int(match_dict["level"]),
            slug=match_dict["slug"],
            text=match_dict["text"],
            index=match.start(),
        )
        for match in HEADING_ELEMENT_REGEX.finditer(html)
        if (match_dict := match.groupdict())
    ]
    return {heading_level: [h for h in heading_elements if h.level == heading_level] for heading_level in range(2, 7)}


def create_toc_section(level: int, start: int, end: int, heading_map: HeadingMap) -> list[TocSection]:
    level_map = [h for h in heading_map[level] if (h.index >= start and end > h.index)]
    if not level_map or not len(level_map):
        return []
    toc: list[TocSection] = []
    for i, heading in enumerate(level_map):
        section_start = heading.index
        section_end = (level_map[i + 1].index or 0) - 1 if i < len(level_map) - 1 else end
        children = create_toc_section(level + 1, section_start, section_end, heading_map)
        toc.append(TocSection(heading, children))
    return toc


def create_toc_section_html(section: TocSection) -> str:
    indent = 1 if section.heading.level == 2 else 3 if section.heading.level == 3 else 5
    tab = chr(ord("\t"))
    html = f"{tab * indent}<li>\n"
    html += f'{tab * (indent + 1)}<a href="#{section.heading.slug}">{section.heading.text}</a>\n'
    if section.children:
        html += f"{tab * (indent + 1)}<ul>\n"
        for sub_toc in section.children:
            html += create_toc_section_html(sub_toc)
        html += f"{tab * (indent + 1)}</ul>\n"
    html += f"{tab * indent}</li>\n"
    return html
