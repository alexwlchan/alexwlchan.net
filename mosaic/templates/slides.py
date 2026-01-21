"""
Insert slides into blog posts.

This uses my {% picture %} tag, which is defined by another plugin --
it gets wrapped in some presets and common values.  It reuses the logic
from that plugin to create smaller sizes/formats to reduce page weight.

== Example ==

This is how to use the tag:

    {%
      slide
      filename="slide82.png"
      alt="A screenshot of a messaging app."
      caption="Image from Pexels, CC0"
    %}

It looks for the image in a subdirectory of `_images` based on the
year and slug of the post, e.g. if this is a 2018 post `anti-social-media`,
then it looks for the image in `_images/2018/anti-social-media/slide82.png`

The `caption` field is optional, and displays below the image.  It's useful
for attribution or sourcing that doesn't fit on the slide.

"""

from typing import Any

from jinja2 import pass_context
from jinja2.runtime import Context

from mosaic.text import markdownify

from .jinja_extensions import KwargsExtensionBase
from .pictures import render_picture


class SlideExtension(KwargsExtensionBase):
    """
    Defines the {% slide %} tag to render slide images.
    """

    tags = {"slide"}

    @pass_context
    def render_html(self, *args: Any, **kwargs: Any) -> str:
        """
        Render the slide tag.
        """
        return render_slide(*args, **kwargs)


def render_slide(
    context: Context,
    filename: str,
    caption: str | None = None,
    caller: Any | None = None,
    **kwargs: Any,
) -> str:
    """
    Create the HTML to display a slide.
    """
    deck = context["page"].slug

    if caption is not None:
        figcaption_html = f"<figcaption>{markdownify(caption)}</figcaption>"
    else:
        figcaption_html = ""

    picture_html = render_picture(
        context,
        filename=f"{deck}/{filename}",
        width=450,
        loading="lazy",
        link_to="original",
        **kwargs,
    )

    return (
        '<style type="x-text/scss">\n'
        '  @use "components/slides";\n'
        "</style>\n"
        '<figure class="slide">\n' + picture_html + figcaption_html + "</figure>"
    )
