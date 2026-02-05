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

import re
import textwrap

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


__all__ = ["apply_syntax_highlighting"]


def apply_manual_fixes(highlighted_code: str, lang: str) -> str:
    """
    Apply syntax highlighting fixes that go beyond Pygments, based on
    my code snippets.

    This is hacky and manual, but it should be fine because I'm always
    going to review the output manually.
    """
    # Nested CSS: fix the highlighting of nested elements.
    #
    # This isn't as good as proper support for nesting in Pygments, but
    # that's somewhat complicated so I can do hard-coded fixes -- I'll
    # be reviewing all this output manually anyway.
    if lang == "css":
        # Reclassify the octothrope in an ID selector as part of
        # the name.
        highlighted_code = highlighted_code.replace(
            '<span class="p">#</span><span class="nn">', '<span class="nn">#'
        )

        # Reclassify the dot in a class selector as part of
        # the name.
        highlighted_code = highlighted_code.replace(
            '<span class="p">.</span><span class="nc">', '<span class="nc">.'
        )

        # Reclassify brackets which have been mislabelled because they're
        # inside nested CSS.
        highlighted_code = highlighted_code.replace(
            '<span class="err">{</span>', '<span class="p">{</span>'
        ).replace('<span class="err">}</span>', '<span class="p">}</span>')

        # Reclassify nested selectors which have been labelled as properties
        for tag in ("a", "figcaption", "figure", "img", "li"):
            if tag not in highlighted_code:
                continue

            highlighted_code = highlighted_code.replace(
                f'<span class="err">{tag},</span>',
                f'<span class="n">{tag}</span><span class="o">,</span>',
            )
            highlighted_code = highlighted_code.replace(
                f'<span class="err">{tag}</span>', f'<span class="n">{tag}</span>'
            )

        highlighted_code = re.sub(
            r'<span class="err">(?P<classname>\.[a-z]+)</span>',
            r'<span class="nn">\g<classname></span>',
            highlighted_code,
        )

        # Reclassify units as part of numeric constants.
        for unit in ("px", "em", "%"):
            highlighted_code = re.sub(
                r'<span class="mi">(?P<amount>[0-9]+)</span>'
                + f'<span class="kt">{unit}</span>',
                f'<span class="mi">\\g<amount>{unit}</span>',
                highlighted_code,
            )

    # Swift: the shebang at the start is punctuation, not a comment or
    # a name worth highlighting.
    if lang == "swift":
        highlighted_code = highlighted_code.replace(
            '<span class="p">#</span><span class="o">!/</span>'
            '<span class="n">usr</span><span class="o">/</span>'
            '<span class="n">bin</span><span class="o">/</span>'
            '<span class="n">env</span><span class="w"> </span>'
            '<span class="n">swift</span>\n',
            '<span class="p">#!/usr/bin/env swift</span>\n',
        )

    # Python: the shebang at the start is punctuation.
    if lang == "python":
        highlighted_code = highlighted_code.replace(
            '<span class="ch">#!/usr/bin/env python3</span>',
            '<span class="p">#!/usr/bin/env python3</span>',
        )

    # Python console: expand gr (Generic.Error) snippets to include
    # the entire line.
    if lang == "pycon":
        highlighted_code = re.sub(
            r'<span class="gr">(?P<error>[^<]+)</span>: <span class="n">',
            r'<span class="gr">\g<error>: ',
            highlighted_code,
        )

    # Whitespace: delete it unless we're in console or irb snippets,
    # where we use it as part of disabling selection.
    if lang not in {"console", "irb"}:
        highlighted_code = WHITESPACE_RE.sub(r"\g<space>", highlighted_code)

    return highlighted_code


# Matches whitespace tokens, e.g. <span class="w"> </span>
WHITESPACE_RE = re.compile(r'<span class="w">(?P<space>[\s]+)</span>')


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

    # In console snippets, the only prompt character I use is a dollar ($),
    # but the lexer allows # and %.
    #
    # This branch removes those two characters from the regex.  To detect
    # unrelated changes to the regex that I should incorporate, assert the
    # current value of the regex first.
    if lang == "console":
        assert lexer._ps1rgx == re.compile(  # type: ignore
            r"^((?:(?:\[.*?\])|(?:\(\S+\))?(?:| |sh\S*?|\w+\S+[@:]\S+(?:\s+\S+)"
            r"?|\[\S+[@:][^\n]+\].+))\s*[$#%]\s*)(.*\n?)"
        ), "outdated console lexer regex"
        lexer._ps1rgx = re.compile(  # type: ignore
            r"^((?:(?:\[.*?\])|(?:\(\S+\))?(?:| |sh\S*?|\w+\S+[@:]\S+(?:\s+\S+)"
            r"?|\[\S+[@:][^\n]+\].+))\s*[$]\s*)(.*\n?)"
        )

    html = highlight(src, lexer, formatter)
    html = apply_manual_fixes(html, lang)

    if debug:
        print(repr(html))

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

    for idx, m in reversed(list(enumerate(name_matches, start=1))):
        # In HTML, all tags and attributes get highlighted in blue;
        # skip doing any name cleanup.
        if lang == "html" or lang == "xml":
            continue

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
