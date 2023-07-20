from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.config import ROOT_FOLDER
from app.docs.api_docs.content.block import BLOCK_ENDPOINTS, UNICODE_BLOCK_OBJECT_INTRO, UNICODE_BLOCK_OBJECT_PROPERTIES
from app.docs.api_docs.content.character import (
    CHARACTER_ENDPOINTS,
    PROP_GROUP_BASIC,
    PROP_GROUP_BIDIRECTIONALITY,
    PROP_GROUP_CASE,
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
    UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1,
    UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2,
    UNICODE_CHARACTER_PROP_GROUPS_INTRO,
    UNICODE_CHATACTER_OBJECT_INTRO,
    VERBOSITY,
)
from app.docs.api_docs.content.intro import INTRODUCTION, LOOSE_MATCHING, PAGINATION, PROJECT_LINKS_README, SEARCH
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


def create_details_element_readme(title: str, content: str, open: bool | None = False) -> str:
    open_tag = "<details open>" if open else "<details>"
    return f"""\t\t{open_tag}
            <summary style="list-style: none; align-items: center">
                <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                    <div style="height: 16px; transition: transform 0.3s ease-in">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                            <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                        </svg>
                    </div>
                </div>
                <strong style="flex: 1">{title}</strong>
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
    + '\n\t\t<h4 id="verbosity">Verbosity</h4>\n'
    + f"\t\t{VERBOSITY}\n"
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
    + f'{create_details_element_readme("<strong>CJK Variants</strong>", PROP_GROUP_CJK_VARIANTS)}'
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


def create_toc_for_readme() -> str:
    html = get_api_docs_for_readme()
    toc = create_toc_section(2, 0, len(html), create_html_heading_map(html))
    html = '<ul class="toc">\n'
    for section in toc:
        html += create_toc_section_html(section, 0)
    html += "</ul>\n"
    return html


def create_html_heading_map(html: str) -> HeadingMap:
    heading_elements = [
        HtmlHeading(
            level=int(match.groupdict()["level"]),
            slug=match.groupdict()["slug"],
            text=match.groupdict()["text"],
            index=match.start(),
        )
        for match in HEADING_ELEMENT_REGEX.finditer(html)
    ]
    return {heading_level: [h for h in heading_elements if h.level == heading_level] for heading_level in range(2, 7)}


def create_toc_section(level: int, section_start: int, section_end: int, heading_map: HeadingMap) -> list[TocSection]:
    level_map = [h for h in heading_map[level] if (h.index >= section_start and section_end > h.index)]
    if not level_map or not len(level_map):
        return []
    toc: list[TocSection] = []
    for i, heading in enumerate(level_map):
        if i < len(level_map) - 1:
            end = (level_map[i + 1].index or 0) - 1
        else:
            end = section_end
        toc.append(TocSection(heading=heading, children=create_toc_section(level + 1, heading.index, end, heading_map)))
    return toc


def create_toc_section_html(section: TocSection, indent_count: int) -> str:
    html = ("\t" * (indent_count + 1)) + "<li>\n"
    html += ("\t" * (indent_count + 2)) + f'<a href="#{section.heading.slug}">{section.heading.text}</a>\n'
    if section.children:
        html += ("\t" * (indent_count + 2)) + "<ul>\n"
        for sub_toc in section.children:
            html += create_toc_section_html(sub_toc, indent_count + 2)
        html += ("\t" * (indent_count + 2)) + "</ul>\n"
    html += ("\t" * (indent_count + 1)) + "</li>\n"
    return html
