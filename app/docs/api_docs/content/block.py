# flake8: noqa
BLOCK_ENDPOINTS = """
        <dl>
            <dt><strong>GET</strong> <code>/v1/blocks/{name}</code></dt>
            <dd>Retrieve one or more Block(s)</dd>
            <dt><strong>GET</strong> <code>/v1/blocks</code></dt>
            <dd>List Blocks</dd>
            <dt><strong>GET</strong> <code>/v1/blocks/search</code></dt>
            <dd>Search Blocks</dd>
        </dl>
"""

UNICODE_BLOCK_OBJECT_INTRO = (
    "<p>The <code>UnicodeBlock</code> object represents a grouping of characters within the Unicode encoding space. Each block is generally, but not always, meant to supply glyphs used by one or more specific languages, or in some general application area such as mathematics, surveying, decorative typesetting, social forums, etc.</p>"
    + "<p>Each block is a uniquely named, continuous, non-overlapping range of code points, containing a multiple of 16 code points (additionally, the starting codepoint for each block is a multiple of 16). A block may contain unassigned code points, which are reserved.</p>"
    + "<p>The <code>UnicodeBlock</code> object exposes a small set of properties such as the official name of the block, the range of code points assigned to the block and the total number of defined characters within the block:</p>"
)

UNICODE_BLOCK_OBJECT_PROPERTIES = """
            <dl>
                <dt><strong>id</strong></dt>
                <dd><strong><i>This is NOT a property from the Unicode Standard.</i></strong> This is an integer value used to navigate within a paginated list of <code>UnicodeBlock</code> objects. The first block (<code>U+0000..U+007F <span>BASIC LATIN</span></code>) has <code>id=1</code> and each block is numbered sequentially in order of starting codepoint.</dd>
                <dt><strong>name</strong></dt>
                <dd>Unicode blocks are identified by unique names, which use only ASCII characters and are usually descriptive of the nature of the symbols (in English), such as "Tibetan" or "Supplemental Arrows-A".</dd>
                <dt><strong>plane</strong></dt>
                <dd>A string value equal to the abbreviated name of the Unicode Plane containing the block (e.g., "BMP" for Basic Multilingual Plane).</dd>
                <dt><strong>start</strong></dt>
                <dd>A string value equal to the first codepoint allocated to the block, expressed in <code>U+hhhhhh</code> format.</dd>
                <dt><strong>finish</strong></dt>
                <dd>A string value equal to the last codepoint allocated to the block, expressed in <code>U+hhhhhh</code> format.</dd>
                <dt><strong>total_allocated</strong></dt>
                <dd>An integer value equal to the total number of characters (defined or reserved) contained in the block.</dd>
                <dt><strong>total_defined</strong></dt>
                <dd>An integer value equal to the total number of characters with defined names, glyphs, etc in the block.</dd>
            </dl>
"""
