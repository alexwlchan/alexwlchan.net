"""
Tests for `mosaic.syntax_highlighting`.
"""

import pytest

from mosaic.syntax_highlighting import apply_syntax_highlighting
from mosaic.text import markdownify


def test_syntax_highlighting() -> None:
    """
    Test a snippet of syntax highlighting.
    """
    html = markdownify(
        "This is some text\n\n"
        '```python {"debug": false}\n'
        "def greeting(name: str) -> None:\n"
        '    print(f"Hello {name}!")\n'
        "```\n\n"
        "This is some more text\n\n"
        "*   This is a bulleted list\n\n"
        "    ```python\n"
        "    def add(x: int, y: int) -> int:\n"
        "        return x + y\n"
        "    ```"
    )

    assert html == (
        # This is some text
        "<p>This is some text</p>\n"
        '<pre class="lng-python"><code>'
        # def greeting
        '<span class="k">def</span> greeting'
        # (name
        '<span class="p">(</span>name'
        # : str)
        '<span class="p">:</span> str<span class="p">)</span> '
        # -> None
        '<span class="o">-&gt;</span> <span class="kc">None</span>'
        # :
        '<span class="p">:</span>\n    '
        # print(
        'print<span class="p">(</span>'
        # "Hello
        '<span class="sa">f</span><span class="s2">&quot;Hello </span>'
        # {name}
        '<span class="si">{</span>name<span class="si">}</span>'
        # !")
        '<span class="s2">!&quot;</span><span class="p">)</span>'
        "</code></pre>\n"
        # This is some more text
        "<p>This is some more text</p>\n<ul>\n<li>"
        # This is a bulleted list
        "<p>This is a bulleted list</p>\n"
        '<pre class="lng-python"><code>'
        # def
        '<span class="k">def</span> '
        # add(
        'add<span class="p">(</span>'
        # x: int
        'x<span class="p">:</span> int'
        # , y:
        '<span class="p">,</span> y<span class="p">:</span> '
        # int)
        'int<span class="p">)</span> '
        # ->
        '<span class="o">-&gt;</span> '
        # int:
        'int<span class="p">:</span>\n'
        # return x +
        '    <span class="k">return</span> x '
        # + y
        '<span class="o">+</span> y</code></pre>'
        "\n</li>\n</ul>"
    )


def test_syntax_highlighting_is_not_greedy() -> None:
    """
    Syntax highlighting does a non-greedy match on the code.
    """
    html = markdownify(
        "This is some text\n"
        "\n"
        '```python {"debug": true}\n'
        "def greeting(name: str) -> None:\n"
        '    print(f"Hello {name}!")\n'
        "```\n"
        "\n"
        "This is some more text\n"
        "\n"
        "```python\n"
        "def add(x: int, y: int) -> int:\n"
        "    return x + y\n"
        "```"
    )

    assert "<p>This is some more text</p>" in html


def test_fenced_code_block_without_lang_is_still_pre() -> None:
    """
    A fenced code block without a language is still wrapped in <pre> tags.
    """
    html = markdownify(
        "This is some text\n"
        "\n"
        "```\n"
        "line 1\n"
        "line 2\n"
        "```\n\n"
        "This is some more text\n\n"
        "```\n"
        "line 3\n"
        "line 4\n"
        "```"
    )

    assert html == (
        "<p>This is some text</p>\n"
        '<pre class="lng-text"><code>line 1\nline 2</code></pre>\n'
        "<p>This is some more text</p>\n"
        '<pre class="lng-text"><code>line 3\nline 4</code></pre>'
    )


def test_syntax_highlighting_with_indent() -> None:
    """
    We handle empty lines in indented code blocks.
    """
    html = markdownify(
        "This is some text\n"
        "\n"
        "```python\n"
        "def add(x, y):\n"
        "    return x + y\n"
        "\n"
        "def greeting(name)\n"
        '    print(f"Hello {name}!")\n'
        "```\n"
        "\n"
        "*   This is a bulleted list\n"
        "\n"
        "    ```python\n"
        "    def add(x, y)\n"
        "        return x + y\n"
        "\n"
        "    def greeting(name)\n"
        '        print(f"Hello {name}!")\n'
        "    ```"
    )

    assert html == (
        "<p>This is some text</p>\n"
        '<pre class="lng-python"><code>'
        # def add(x, y):
        '<span class="k">def</span> add'
        '<span class="p">(</span>x<span class="p">,</span> '
        'y<span class="p">):</span>\n'
        # return x + y
        '    <span class="k">return</span> x <span class="o">+</span> y\n'
        "\n"
        # def greeting(name)
        '<span class="k">def</span> '
        'greeting<span class="p">(</span>'
        'name<span class="p">)</span>\n'
        # print(f"Hello {name}!")
        '    print<span class="p">(</span>'
        '<span class="sa">f</span><span class="s2">&quot;Hello </span>'
        '<span class="si">{</span>name<span class="si">}</span>'
        '<span class="s2">!&quot;</span><span class="p">)</span>'
        "</code></pre>"
        "\n"
        "<ul>\n<li>"
        "<p>This is a bulleted list</p>\n"
        '<pre class="lng-python"><code>'
        # Notice this second block uses <br/> instead of \n
        # def add(x, y):
        '<span class="k">def</span> add'
        '<span class="p">(</span>x<span class="p">,</span> '
        'y<span class="p">)</span>\n'
        # return x + y
        '    <span class="k">return</span> x <span class="o">+</span> y\n'
        "\n"
        # def greeting(name):
        '<span class="k">def</span> '
        'greeting<span class="p">(</span>'
        'name<span class="p">)</span>\n'
        # print(f"Hello {name}!")
        '    print<span class="p">(</span>'
        '<span class="sa">f</span><span class="s2">"Hello </span>'
        '<span class="si">{</span>name<span class="si">}</span>'
        '<span class="s2">!"</span><span class="p">)</span>'
        "</code></pre>\n</li>\n</ul>"
    )


def test_throws_if_mismatched_varname() -> None:
    """
    Highlighting a name which doesn't match the source code is an error.
    """
    with pytest.raises(ValueError, match="bad name"):
        apply_syntax_highlighting(src="x = x + 1", lang="python", names={1: "y"})


def test_highlighting_name() -> None:
    """
    Highlighting a name wraps it in <span class="n">.
    """
    html_no_name = markdownify("```python\nx = y + 1\n```")
    assert html_no_name == (
        '<pre class="lng-python"><code>'
        'x <span class="o">=</span> y <span class="o">+</span> '
        '<span class="mi">1</span></code></pre>'
    )

    html_name = markdownify('```python {"names": {"1": "x"}}\nx = y + 1\n```')
    assert html_name == (
        '<pre class="lng-python"><code>'
        '<span class="n">x</span> <span class="o">=</span> y <span class="o">+</span> '
        '<span class="mi">1</span></code></pre>'
    )


@pytest.mark.parametrize(
    "src, names, must_include",
    [
        # Class and ID selectors include the leading octothorpe/dot
        ("#fires { color: red; }", {1: "#fires"}, '<span class="n">#fires</span>'),
        (".forest { color: green; }", {1: ".forest"}, '<span class="n">.forest</span>'),
        #
        # Nested selectors should be highlighted properly
        (
            "figure { .nested { color: pink; } }",
            {1: "figure", 2: ".nested"},
            '<span class="n">.nested</span>',
        ),
        (
            ".nested { a, img { color: yellow; } }",
            {1: ".nested", 2: "a", 3: "img"},
            '<span class="n">a</span><span class="o">,</span> '
            '<span class="n">img</span>',
        ),
        #
        # Units should be highlighted as part of a number.
        ("p { margin: 5px; }", {}, '<span class="mi">5px</span>'),
    ],
)
def test_css_highlighting(src: str, names: dict[int, str], must_include: str) -> None:
    """
    Test the manual fixes for CSS highlighting.
    """
    html = apply_syntax_highlighting(src, lang="css", names=names)
    assert must_include in html
    assert '<span class="err">' not in html


def test_swift_shebang_is_not_highlighted() -> None:
    """
    The shebang at the start of a Swift script is punctuation.
    """
    html = apply_syntax_highlighting(
        src='#!/usr/bin/env swift\n\nprint("Hello world")', lang="swift"
    )
    assert html.startswith(
        '<pre class="lng-swift"><code><span class="p">#!/usr/bin/env swift</span>'
    )


def test_console_preserves_whitespace() -> None:
    """
    Whitespace tokens are preserved in console snippets.
    """
    html = apply_syntax_highlighting(src='$ echo "hello world"', lang="console")
    assert '<span class="gp">$ </span>echo<span class="w"> </span>' in html


def test_console_does_not_highlight_hash_in_output() -> None:
    """
    The console language only highlights $ as the prompt, not #.
    """
    html = apply_syntax_highlighting(
        src='$ echo "# hello world"\n# hello world', lang="console"
    )
    assert '<span class="gp"># </span>' not in html


def test_pycon_traceback() -> None:
    """
    In a traceback in the Python console, the error message is included
    in the traceback.
    """
    src = (
        '>>> raise ValueError("BOOM!")\n'
        "Traceback (most recent call last):\n"
        "[…]\n"
        "ValueError: BOOM!\n"
        ">>> 1 + 2\n"
        "3"
    )
    html = apply_syntax_highlighting(src, lang="pycon")
    assert '<span class="gr">ValueError: BOOM!</span>' in html
