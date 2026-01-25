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
import textwrap

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

    # Find all the names which are highlighted as part of this code.
    name_matches = re.finditer(
        r'<span class="n[a-z0]?">(?P<varname>[^<]+)</span>', html
    )

    # Un-highlight any names that aren't explicitly labelled as worth
    # highlighting.
    if names is not None:
        names_to_highlight = names
    else:
        names_to_highlight = {}

    # print(repr(names_to_highlight))

    for idx, m in reversed(list(enumerate(name_matches, start=1))):
        varname = m.group("varname")
        start, end = m.start(), m.end()

        # If we're in debug mode, add a checkbox and a <label> that can
        # be used to toggle names.
        #
        # This allows me to build the colouring interactively.
        if debug:
            form_id = f"{idx}:{varname}"
            html = (
                html[:start]
                + (
                    f'<label for="{form_id}">{varname}'
                    f'<input class="codeName" type="checkbox" id="{form_id}" '
                    f'data-idx="{idx}" data-varname="{varname}" '
                    f'onChange="recalculateVariables()"/></label>'
                )
                + html[end:]
            )
            continue

        # If this isn't a name we want to highlight, remove the
        # <span class="n*"> and continue.
        if names_to_highlight.get(idx) is None:
            html = html[:start] + varname + html[end:]

        # If this is one of the names we want to highlight but the variable
        # name doesn't match, throw an error.
        elif names_to_highlight[idx] != varname:
            raise ValueError(
                f"got bad name at {idx}: want {names_to_highlight[idx]}, got {varname}"
            )

        # Rewrap in <span class="n">, so the name is highlighted.
        else:
            html = html[:start] + f'<span class="n">{varname}</span>' + html[end:]

    # Remove the wrapper <div> applied by Pygments
    html = re.sub(r'^<div class="highlight">', "", html)
    html = re.sub("</div>$", "", html)

    # Insert an inner <code> block inside the <pre> tag
    html = re.sub(r"^<pre>", f'<pre class="lng-{lang}"><code>', html)
    html = re.sub(r"\s*</pre>$", "</code></pre>", html)

    html = html.replace("<span></span>", "")

    # If we're in debug mode, append the debugging snippet.
    #
    # This gives me a tool that lets my dynamically choose which names
    # to highlight, and constructs the `names` string I should add
    # to my code.
    if debug:
        html += textwrap.dedent("""
            <p id="debug">DEBUG: <code id="debugNames">names=""</code></p>
            <style>
              pre input[type="checkbox"] {
                display: none;
              }

              pre label {
                text-decoration: underline;
                -webkit-text-decoration-style: dashed;
              }

              pre label:has(input[type="checkbox"]:checked) {
                color: var(--blue);
              }

              #debug {
                color: red;
              }
            </style>
            <script>
              function recalculateVariables() {
                debugNames = document.querySelector("code#debugNames");

                var selectedNames = {};

                document.querySelectorAll("input.codeName")
                  .forEach(checkbox => {
                    if (checkbox.checked) {
                      selectedNames[checkbox.getAttribute('data-idx')] = 
                        checkbox.getAttribute('data-varname');
                    }
                  });

                debugNames.innerText = JSON.stringify({"names": selectedNames});
              }
            </script>
        """)

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
        r"(?P<lang>[a-z\-]+)?"             # language name
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
                print(repr(m.group("attrs")))
                highlighter_args = json.loads(m.group("attrs"))
            else:
                highlighter_args = {}

            if "names" in highlighter_args:
                highlighter_args["names"] = {
                    int(idx): name for idx, name in highlighter_args["names"].items()
                }

            if m.group("indent"):
                src = "\n".join(
                    re.sub(r"^" + m.group("indent"), "", line)
                    for line in m.group("src").splitlines()
                )
            else:
                src = m.group("src")

            html = apply_syntax_highlighting(
                src,
                lang=m.group("lang") or "text",
                **highlighter_args,
            )

            # If the original Markdown was indented, collapse all the
            # newlines into <br/> tags.
            #
            # This means Python-Markdown will treat it as a single HTML
            # element, and won't break it into separate paragraphs.
            if m.group("indent"):
                assert html.endswith("\n")
                html = html.rstrip().replace("\n", "<br/>")
                assert not html.endswith("\n")

            text = text.replace(m.group(0), m.group("indent") + html)

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
