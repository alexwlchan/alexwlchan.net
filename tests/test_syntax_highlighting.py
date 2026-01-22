"""
Tests for `mosaic.syntax_highlighting`.
"""

from markdown import markdown

from mosaic.syntax_highlighting import SyntaxHighlighterExtension


def test_syntax_highlighting() -> None:
    """
    Test a snippet of syntax highlighting.
    """
    html = markdown(
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
        "    ```",
        extensions=[SyntaxHighlighterExtension()],
    )

    assert html == (
        # This is some text
        "<p>This is some text</p>\n"
        '<pre class="lng-python"><code>'
        # def
        '<span class="k">def</span><span class="w"> </span>'
        # greeting
        "greeting"
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
        "</code></pre>\n\n"
        # This is some more text
        "<p>This is some more text</p>\n<ul>\n<li>\n"
        # This is a bulleted list
        "<p>This is a bulleted list</p>\n<p>"
        '<pre class="lng-python"><code>'
        # def
        '<span class="k">def</span><span class="w"> </span>'
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
        'int<span class="p">:</span><br/>    '
        # return x +
        '<span class="k">return</span> x '
        # + y
        '<span class="o">+</span> y</code></pre>'
        "</p>\n</li>\n</ul>"
    )


def test_syntax_highlighting_is_not_greedy() -> None:
    """
    Syntax highlighting does a non-greedy match on the code.
    """
    html = markdown(
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
        "```",
        extensions=[SyntaxHighlighterExtension()],
    )

    assert "<p>This is some more text</p>" in html


def test_fenced_code_block_without_lang_is_still_pre() -> None:
    """
    A fenced code block without a language is still wrapped in <pre> tags.
    """
    html = markdown(
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
        "```",
        extensions=[SyntaxHighlighterExtension()],
    )

    assert html == (
        "<p>This is some text</p>\n"
        '<pre class="lng-text"><code>line 1\nline 2</code></pre>\n\n'
        "<p>This is some more text</p>\n"
        '<pre class="lng-text"><code>line 3\nline 4</code></pre>'
    )


def test_syntax_highlighting_with_indent() -> None:
    """
    We handle empty lines in indented code blocks.
    """
    html = markdown(
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
        "    ```",
        extensions=[SyntaxHighlighterExtension()],
    )

    assert html == (
        "<p>This is some text</p>\n"
        '<pre class="lng-python"><code>'
        # def add(x, y):
        '<span class="k">def</span><span class="w"> </span>add'
        '<span class="p">(</span>x<span class="p">,</span> '
        'y<span class="p">):</span>\n'
        # return x + y
        '    <span class="k">return</span> x <span class="o">+</span> y\n'
        "\n"
        # def greeting(name)
        '<span class="k">def</span><span class="w"> </span>'
        'greeting<span class="p">(</span>'
        'name<span class="p">)</span>\n'
        # print(f"Hello {name}!")
        '    print<span class="p">(</span>'
        '<span class="sa">f</span><span class="s2">&quot;Hello </span>'
        '<span class="si">{</span>name<span class="si">}</span>'
        '<span class="s2">!&quot;</span><span class="p">)</span>'
        "</code></pre>\n"
        "\n"
        "<ul>\n<li>\n"
        "<p>This is a bulleted list</p>\n"
        '<p><pre class="lng-python"><code>'
        # Notice this second block uses <br/> instead of \n
        # def add(x, y):
        '<span class="k">def</span><span class="w"> </span>add'
        '<span class="p">(</span>x<span class="p">,</span> '
        'y<span class="p">)</span><br/>'
        # return x + y
        '    <span class="k">return</span> x <span class="o">+</span> y<br/>'
        "<br/>"
        # def greeting(name):
        '<span class="k">def</span><span class="w"> </span>'
        'greeting<span class="p">(</span>'
        'name<span class="p">)</span><br/>'
        # print(f"Hello {name}!")
        '    print<span class="p">(</span>'
        '<span class="sa">f</span><span class="s2">&quot;Hello </span>'
        '<span class="si">{</span>name<span class="si">}</span>'
        '<span class="s2">!&quot;</span><span class="p">)</span>'
        "</code></pre></p>\n</li>\n</ul>"
    )
