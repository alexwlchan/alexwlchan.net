"""
Tests for `mosaic.templates.updates`.
"""

from jinja2 import Environment


def test_render_update(env: Environment) -> None:
    """
    Test the basic usage of the {% update %} tag.
    """
    md = (
        '{% update date="2001-02-03" %}\n'
        "  I am *really* excited about this change.\n"
        "{% endupdate %}\n"
    )

    html = env.from_string(md).render().strip()
    assert html == (
        '<style type="x-text/scss">\n'
        '  @use "components/updates";\n'
        "</style>\n"
        '<blockquote class="update" id="update-2001-02-03">\n'
        '<p><strong>Update, <time datetime="2001-02-03">'
        "3 February 2001</time>:</strong> "
        "I am <em>really</em> excited about this change.</p>\n"
        "</blockquote>"
    )


def test_update_with_code(env: Environment) -> None:
    """
    Test rendering of an {% update %} with inline code.
    """
    md = (
        '{% update date="2001-02-03" %}\n'
        "  ```python\n"
        "  from __future__ import print_function\n"
        "\n"
        "  print('Hello world!')\n"
        "  ```\n"
        "{% endupdate %}\n"
    )

    html = env.from_string(md).render().strip()
    assert "\n\n" not in html
