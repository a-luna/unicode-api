# flake8: noqa
CODEPOINTS_ENDPOINT = """
        <dl>
            <dt><strong>GET</strong> <code>/v1/codepoints/{hex}</code></dt>
            <dd>Retrieve details of a single character</dd>
        </dl>
"""

CODEPOINT_CONTENT = (
    "<p>The <code>UnicodeCodepoint</code> resource is not an object like the other resources, it is simply a hexadecimal value that refers to a single character in the Unicode codespace. </p>"
    + "<p>This endpoint performs nearly the same function as the <code>/v1/characters/{string}</code> endpoint. However, sending a request for a character to the <code>/v1/characters/{string}</code> endpoint requires you to provide either the character itself or the URI encoded string representation of the character.</p>"
    + "<p>Since there are plenty of scenarios where it may be easier to supply the assigned codepoint for a character rather than the rendered glyph or URI-encoded value, the <code>/v1/codepoints/{hex}</code> endpoint allows you to request the same sets of character property groups as the <code>/v1/characters/{string}</code> endpoint.</p>"
    + "<p>The only difference between the two endpoints is requests to the <code>/v1/characters/{string}</code> endpoint can retrieve data for one or more characters, while requests to the <code>/v1/codepoints/{hex}</code> endpoint can only be used to retrieve details of a single character.</p>"
)
