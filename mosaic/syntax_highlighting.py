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
from typing import Literal

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
    # Remove empty spans
    highlighted_code = highlighted_code.replace("<span></span>", "")

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
        highlighted_code = re.sub(
            r'<span class="mi">(?P<amount>\-?[0-9]+)</span>'
            r'<span class="kt">(?P<unit>deg|em|px|vh|%)</span>',
            r'<span class="mi">\g<amount>\g<unit></span>',
            highlighted_code,
        )

    # Python: dotted imports should be replaced with names split by
    # namespace. nn = Name.Namespace
    if lang == "python":
        for m in re.finditer(
            r'<span class="nn">(?P<name>[a-zA-Z0-9_]+\.[a-zA-Z0-9_\.]+)</span>',
            highlighted_code,
        ):
            import_name = m.group("name")
            parts = import_name.split(".")
            dot = '<span class="p">.</span>'
            highlighted_code = highlighted_code.replace(
                m.group(0),
                dot.join(f'<span class="n">{name}</span>' for name in parts),
            )

    # Python: magic methods should be regular names.
    if lang == "python":
        highlighted_code = highlighted_code.replace(
            '<span class="fm">', '<span class="n">'
        )

    # Swift: the opening hashbang should be a Comment.Hashbang.
    if lang == "swift":
        highlighted_code = highlighted_code.replace(
            '<span class="p">#</span><span class="o">!/</span>'
            '<span class="n">usr</span><span class="o">/</span>'
            '<span class="n">bin</span><span class="o">/</span>'
            '<span class="n">env</span><span class="w"> </span>'
            '<span class="n">swift</span>\n',
            '<span class="ch">#!/usr/bin/env swift</span>\n',
        )

    # Bash: highlight functions as potential names
    if lang == "bash":
        highlighted_code = re.sub(
            r'(<pre>|\n)(?P<function_name>[a-z_]+)(<span class="o">\(\)</span>)',
            r'\1<span class="n">\g<function_name></span>\3',
            highlighted_code,
            flags=re.MULTILINE,
        )

    # Python console: expand gr (Generic.Error) snippets to include
    # the entire line.
    if lang == "pycon":
        highlighted_code = re.sub(
            r'<span class="gr">(?P<error>[^<]+)</span>: <span class="n">',
            r'<span class="gr">\g<error>: ',
            highlighted_code,
        )

    # Python console: unhighlighted lines that start with 'File' in
    # the traceback are gr (Generic.Error).
    if lang == "pycon":
        all_lines = highlighted_code.splitlines()
        for i, line in enumerate(all_lines):
            if line.startswith("  File"):
                line = re.sub(
                    r'line <span class="m">(?P<lineno>[0-9]+)</span>',
                    r"line \g<lineno>",
                    line,
                )
                all_lines[i] = f'<span class="gr">{line}</span>'
        highlighted_code = "\n".join(all_lines)

    # C: highlight macro names as variable names
    # cp = Comment.Preproc
    if lang == "c":
        highlighted_code = re.sub(
            r'<span class="cp">(?P<define>#\s*define) '
            r"(?P<name>[A-Z_]+)\((?P<args>[^\)]+)\)",
            r'\g<define> <span class="n">\g<name></span>'
            r'<span class="p">(</span>\g<args><span class="p">)</span>',
            highlighted_code,
        )

    # C: highlight #define variables as variable names.
    # cp = Comment.Preprox
    # mi = Number.Integer
    if lang == "c":
        highlighted_code = re.sub(
            r'<span class="cp">(?P<define>#\s*define) '
            r"(?P<name>[A-Z_]+) (?P<value>[0-9]+)</span>",
            r'\g<define> <span class="n">\g<name></span> '
            r'<span class="mi">\g<value></span>',
            highlighted_code,
        )
        highlighted_code = re.sub(
            r'<span class="cp">(?P<define>#\s*define) '
            r"(?P<name>[A-Z_]+) (?P<value>[A-Za-z\(\)]+)</span>",
            r'\g<define> <span class="n">\g<name></span> \g<value>',
            highlighted_code,
        )

    # Fish: highlight variable names after `set`
    if lang == "fish":
        highlighted_code = re.sub(
            r'<span class="([a-z]+)">(?P<keyword>set|function)</span>'
            r"(?P<flags>(?: -g| -x)*) "
            r"(?P<name>[A-Za-z0-9_]+)(?P<space>\s)",
            r'\g<keyword>\g<flags> <span class="n">\g<name></span>\g<space>',
            highlighted_code,
            flags=re.MULTILINE,
        )

    # Terraform: the 'resource' keyword is not worth highlighting.
    if lang == "terraform":
        highlighted_code = highlighted_code.replace(
            '<span class="kr">resource</span>', "resource"
        )

    # TypeScript: the 'type' keyword is not worth highlighting.
    if lang == "typescript":
        highlighted_code = highlighted_code.replace(
            '<span class="kr">type</span>', "type"
        )

    # Whitespace: delete it unless we're in console or irb snippets,
    # where we use it as part of disabling selection.
    if lang not in {"console", "irb", "pycon", "sqlite3"}:
        highlighted_code = WHITESPACE_RE.sub(r"\g<space>", highlighted_code)
    else:
        # Ensure the space immediately after the `gp` is the whitespace
        # which will be ignored for selection, and not something in the
        # middle of the command.
        highlighted_code = highlighted_code.replace(
            '<span class="gp">$ </span>',
            '<span class="gp">$</span><span class="w"> </span>',
        )

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
    line_numbers: str = "",
    caption: str = "",
) -> str:
    """
    Apply syntax highlighting rules to a block of code.

    This has all my custom logic for adding line numbers, tidying up
    the output HTML, and so on. It doesn't know anything about Markdown.
    """
    if lang == "caddy":
        html = format_caddy(src)
    else:
        html = format_with_pygments(src, lang)

    html = apply_manual_fixes(html, lang)

    if debug:
        print(repr(html))

    # Find all the names which are highlighted as part of this code.
    name_matches = re.finditer(
        r'<span class="(n[a-z0]?|cp)">(?P<varname>[^<]+)</span>', html
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
        if (lang in {"caddy", "html", "xml"}) and names is None and not debug:
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
        #
        # In Terraform, it's okay to omit the wrapping quotes because it
        # makes the JSON escaping trickier.
        elif (
            lang == "terraform"
            and "&quot;" + names_to_highlight[idx] + "&quot;" != varname
        ) or (lang != "terraform" and names_to_highlight[idx] != varname):
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
    if wrap:
        html = re.sub(r"^<pre>", f'<pre class="lng-{lang} wrap"><code>', html)
    else:
        html = re.sub(r"^<pre>", f'<pre class="lng-{lang}"><code>', html)
    html = re.sub(r"\s*</pre>$", "</code></pre>", html)

    html = html.replace("<span></span>", "")

    if linenos or line_numbers:
        html, lineno_digits = add_line_numbers(html, linenos, line_numbers)

        if caption:
            figcaption = f"<figcaption>{caption}</figcaption>"
        else:
            figcaption = ""

        html = (
            f'<figure class="annotated_code" '
            f'style="--lineno-digits: {lineno_digits}">'
            f"{html}{figcaption}</figure>"
        )

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
                // Prevent LiveReload from blatting the page when I'm midway
                // through setting variables.
                if (typeof window.LiveReload !== 'undefined') {
                  window.LiveReload.shutDown();
                }
                  
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


def add_line_numbers(html: str, linenos: bool, line_numbers: str) -> tuple[str, int]:
    """
    Add line numbers to the HTML string.

    Returns the highlighted code and the number of digits to allocate
    for line numbering.
    """
    assert linenos or line_numbers

    prefix1, prefix2, remaining = html.partition("<code>")
    inner, suffix1, suffix2 = remaining.rpartition("</code>")
    assert prefix1 + prefix2 + inner + suffix1 + suffix2 == html

    line_count = len(inner.splitlines())

    # If we passed linenos=true but didn't set any line numbers
    # explicitly, default the line numbers to 1–N, where N is the
    # number of lines.
    if not line_numbers:
        line_numbers = f"1-{line_count}"

    # Parse the line_numbers attribute.
    exact_line_numbers = parse_line_numbers(line_numbers)

    # Check we have the correct number of line numbers to pair with
    # each line in the snippet.
    if len(exact_line_numbers) != line_count:
        raise ValueError(
            f"mismatched line numbers: got {len(exact_line_numbers)}, want {line_count}"
        )

    # Wrap each line in a <span class="ln"> (for "line") element
    #
    # e.g. if the input is
    #
    #     <pre>
    #     def greet():
    #         print("hello world!")
    #     </pre>
    #
    # then it becomes
    #
    #     <pre>
    #     <span class="ln">def greet():</span>
    #     <span class="ln">    print("hello world!")</span>
    #     </pre>
    #
    # We look for lines which are just ellipsis, which I often use
    # in code snippets to indicate there's more text that I omitted.
    inner_lines = inner.splitlines()
    numbered_lines = []

    for line, lineno in zip(inner_lines, exact_line_numbers):
        if lineno == "…":
            numbered_lines.append(f'<span class="ln empty p">{line}</span>')
        else:
            numbered_lines.append(
                f'<span class="ln" style="--ln: {lineno}">{line}</span>'
            )

    assert len(numbered_lines) == len(inner_lines)

    html = prefix1 + prefix2 + "\n".join(numbered_lines) + suffix1 + suffix2
    lineno_digits = max(len(str(s)) for s in exact_line_numbers)
    return html, lineno_digits


def parse_line_numbers(s: str) -> list[int | Literal["…"]]:
    """
    Parse a range like 1-3,7-9 as a complete list of line numbers,
    such as [1,2,3,7,8,9].

    The line numbers can include an … character, which indicates the
    line should not be numbered.
    """
    result: list[int | Literal["…"]] = []

    for part in s.split(","):
        if "-" in part:
            start, end = part.split("-")
            for i in range(int(start), int(end) + 1):
                result.append(i)
        elif "–" in part:  # en dash
            start, end = part.split("–")
            for i in range(int(start), int(end) + 1):
                result.append(i)
        elif part == "…":
            result.append("…")
        else:
            result.append(int(part))

    return result


def format_with_pygments(src: str, lang: str) -> str:
    """
    Apply syntax highlighting for a code snippet with Pygments.
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

    return highlight(src, lexer, formatter)


# Matches a line which only contains whitespace and a closing brace
CADDY_CLOSING_PARENS_RE = re.compile(r"^(?P<whitespace>\s*)}$")

# Matches a line which starts with a #
CADDY_COMMENT_RE = re.compile(r"^(?P<whitespace>\s*)# (?P<comment>.*)")

# Matches a line with a matcher at the start of the line
CADDY_MATCHER_RE = re.compile(r"^(?P<matcher>[^\s]+) {$")

# Matches a line with a matcher indented in the line
CADDY_INDENTED_MATCHER_RE = re.compile(r"^(?P<whitespace>\s+)(?P<matcher>[^\s]+) {$")


def format_caddy(src: str) -> str:
    """
    Apply syntax highlighting for Caddy config.

    There's no Pygments lexer, so this is a rough lexer based on my snippets.
    """
    out_lines = []

    for line in src.splitlines():
        # Empty lines are passed unmodified
        if not line.strip():
            out_lines.append("")

        # Any line starting with # is a comment
        elif m := CADDY_COMMENT_RE.match(line):
            out_lines.append(
                m.group("whitespace")
                + '<span class="c"># '
                + m.group("comment")
                + "</span>"
            )

        # Closing parens
        elif m := CADDY_CLOSING_PARENS_RE.match(line):
            out_lines.append(m.group("whitespace") + '<span class="p">}</span>')

        elif m := CADDY_MATCHER_RE.match(line):
            out_lines.append(
                '<span class="n">'
                + m.group("matcher")
                + "</span> "
                + '<span class="p">{</span>'
            )

        elif m := CADDY_INDENTED_MATCHER_RE.match(line):
            out_lines.append(
                m.group("whitespace") + m.group("matcher") + ' <span class="p">{</span>'
            )

        else:
            out_lines.append(line)

    return '<div class="highlight"><pre>' + "\n".join(out_lines) + "</pre></div>"
