# flake8: noqa
from app.core.cache import cached_data

PLANE_ENDPOINTS = """
        <dl>
            <dt><strong>GET</strong> <code>/v1/planes/{number}</code></dt>
            <dd>Retrieve one or more Plane(s)</dd>
            <dt><strong>GET</strong> <code>/v1/planes</code></dt>
            <dd>List Planes</dd>
        </dl>
"""

UNICODE_PLANE_OBJECT_INTRO = (
    "<p>The <code>UnicodePlane</code> object represents a continuous group of <strong>65,536</strong> (2<sup>16</sup>) code points. There are 17 planes, identified by the numbers 0 to 16. The first two positions of a character's codepoint value (U+<strong>hh</strong>hhhh) correspond to the plane number in hex format (possible values <code>0x00</code>–<code>0x10</code>).</p>"
    + '<p>Plane 0 is the <strong>Basic Multilingual Plane (BMP)</strong>, which contains most commonly used characters. The higher planes 1 through 16 are called "supplementary planes". The last code point in plane 16 is the last code point in Unicode, U+10FFFF.</p>'
)


def get_plane_name_list():
    list_items = [
        f"\t\t\t\t\t<li style=\"list-style-type: '{p.number}.'\"><span>{p.name} ({p.abbreviation})</span></li>\n"
        for p in cached_data.planes
    ]
    html = "\t\t\t\t<ol>\n"
    for li in list_items:
        html += li
    html += "\t\t\t\t</ol>"
    return html


UNICODE_PLANE_OBJECT_PROPERTIES = f"""
        <dl>
            <dt><strong>number</strong></dt>
            <dd>The official number that identifies the range of codepoints within a plane. The first two positions of a character's codepoint value (U+<strong>hh</strong>hhhh) correspond to the plane number in hex format (possible values <code>0x00</code>...<code>0x10</code>). This is a decimal value, however, with possible values <strong>0...16</strong>.</dd>
            <dt><strong>name</strong></dt>
            <dd>
                <p>The official name of a plane, according to the Unicode Standard. As of version 15.0.0, seven of the total 17 planes have official names (the official abbreviation for each plane if also given in parentheses):</p>
{get_plane_name_list()}
                <p>The codepoints within Planes 4-13 (<code>U+40000</code>...<code>U+​DFFFF</code>) are unassigned, and these planes currently have no official name/abbreviation.</p>
            </dd>
            <dt><strong>abbreviation</strong></dt>
            <dd>An acronym that identifies the plane, the list in the previous definition contains the abbreviation for each plane along with the official name.</dd>
            <dt><strong>start</strong></dt>
            <dd>A string value equal to the first codepoint allocated to the plane, expressed in <code>U+hhhhhh</code> format.</dd>
            <dt><strong>finish</strong></dt>
            <dd>A string value equal to the last codepoint allocated to the plane, expressed in <code>U+hhhhhh</code> format.</dd>
            <dt><strong>total_allocated</strong></dt>
            <dd>An integer value equal to the total number of characters (defined or reserved) contained in the plane (always 2<sup>16</sup>).</dd>
            <dt><strong>total_defined</strong></dt>
            <dd>An integer value equal to the total number of characters with defined names, glyphs, etc in the plane.</dd>
        </dl>
"""
