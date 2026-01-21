"""
Syntax highlighting for code snippets.

This uses syntax inspired by Python-Markdown:

    ```python {"arg1": true, "arg2": false}
    def greeting(name: str) -> None:
        print(f"Hello, {name}!")
    ```

After the language name is an optional JSON blob where I can pass other
arguments to my syntax highlighting code.

In Python-Markdown, those curly braces are used for extra attributes
instead.
"""

import json
import re

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def apply_syntax_highlighting(
    src: str,
    lang: str,
    names: dict[int, str] | None = None,
    debug: bool = False,
    wrap: bool = False,
    linenos: bool = False,
) -> str:
    """
    Apply syntax highlighting rules to a block of code.

    This has all my custom logic for adding line numbers, tidying up
    the output HTML, and so on. It doesn't know anything about Markdown.
    """
    lexer = get_lexer_by_name(lang)
    formatter = HtmlFormatter()

    html = highlight(src, lexer, formatter)

    # Remove the wrapper <div> applied by Pygments
    html = re.sub(r'^<div class="highlight">', "", html)
    html = re.sub("</div>$", "", html)

    # Insert an inner <code> block inside the <pre> tag
    html = re.sub(r"^<pre>", f'<pre class="lng-{lang}"><code>', html)
    html = re.sub("</pre>$", "</code></pre>", html)

    html = html.replace("<span></span>", "")

    return html


class SyntaxHighlighterPreprocessor(Preprocessor):
    """
    Find and extract fenced code blocks.
    """

    # This matches fenced code blocks like:
    #
    #     ```python {"debug": true, "names": {0: "greet", 1: "name"}}
    #     def greet(name):
    #         print(f"Hello {name}!")
    #     ```
    #
    # fmt: off
    FENCED_BLOCK_RE = re.compile(
        r"^(?P<indent>[ ]*)"              # leading indent
        r"```"                            # opening fence
        r"(?P<lang>[a-z\-]+)"             # language name
        r"(?:[ ](?P<attrs>\{[^\n]+\}))?"  # JSON attributes (optional)
        r"\n"                             # newline (end of opening fence)
        r"(?P<src>.*?)"                   # code content (non-greedy)
        r"(?<=\n)(?P=indent)```",         # closing fence (match opening indent)
        re.MULTILINE | re.DOTALL,
    )
    # fmt: on

    def __init__(self, md: Markdown):
        """
        Create a new instance of SyntaxHighlighterPreprocessor.
        """
        super().__init__(md)

    def run(self, lines: list[str]) -> list[str]:
        """
        Match and store fenced code blocks.
        """
        text = "\n".join(lines)

        while m := self.FENCED_BLOCK_RE.search(text):
            if m.group("attrs"):
                highlighter_args = json.loads(m.group("attrs"))
            else:
                highlighter_args = {}

            if m.group("indent"):
                src = "\n".join(
                    re.sub(r"^" + m.group("indent"), "", line)
                    for line in m.group("src").splitlines()
                )
            else:
                src = m.group("src")

            html = apply_syntax_highlighting(
                src,
                lang=m.group("lang"),
                **highlighter_args,
            )

            if m.group("indent"):
                html = "\n".join(m.group("indent") + line for line in html.splitlines())

            text = text.replace(m.group(0), html)

        return text.split("\n")


class SyntaxHighlighterExtension(Extension):
    """
    Markdown extension to handle syntax highlighting.
    """

    def extendMarkdown(self, md: Markdown) -> None:
        """
        Add `SyntaxHighlighterPreprocessor` to the `Markdown` instance.
        """
        md.registerExtension(self)

        md.preprocessors.register(
            SyntaxHighlighterPreprocessor(md), "syntax_highlighting", 25
        )
