"""
Creates a <picture> tag for images in blog posts.

This is more than a simple <img> tag; it also handles creating
multiple formats and resolutions, to minimise the amount of data
transfer for images in posts.

This includes:

    * Creating copies at different widths from the original, which are
      used with the `srcset` attribute to send copies appropriate for
      different screen resolutions.

    * Creating copies in different formats, including WebP, which have
      better compression and can further reduce data transfer in browsers
      with appropriate support.

    * Creating the HTML markup with the <picture> and <source> tags which
      allows browsers to select an appropriate image.

See:
https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset
https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types

== Example ==

This is a minimal example:

    {%
      picture
      filename="IMG_5744.jpg"
      alt="A black steam engine with a boxy shape."
      width="622"
    %}

It includes the following mandatory parameters:

    * `filename` is the name of the oriignal image.  This should be in
      the same per-year directory as the post.
    * `alt` is the alt text for the image, which must be supplied on
      all posts (which is checked by the linter plugin).
    * `width` or `height`, which is used to pick the sizes for the
      different resolutions.  This is a rough guide.

It will look for the image in `/images/[year]/[filename]`, so if this
was a post from 2022, it will look in `/images/2022/IMG_5744.jpg`.

Other Parameters
----------------
    * `link_to="original"` -- if added, the final <picture> tag will be
      wrapped in an <a> that links to the full-sized image.  Useful for
      gallery-type posts.

    * `link_to="https://example.com/some/page"` -- causes the <a> to link
      to somewhere other than the full-sized image.

    * `parent="/images"` -- looks for an image in somewhere other than
      the per-year directory.

Any other attribute (e.g. `style`, `class`) will be passed directly to
the  underlying <img> tag, which allows you to apply styles or behaviours
not covered by this plugin.

== How it works ==

The code in this file will create the different variants of each image,
based on:

    * dimensions, e.g. if the image is going to be shown at 300px wide,
      it might resize to 300px, 600px and 900px wide versions, to be
      shown on screens with 1x, 2x, 3px pixel density, respectively
    * light/dark mode -- if I have an image "cat.jpg" and a second file
      "cat.dark.jpg", then the latter is used for dark mode

Then it passes all of those variants into my `picture.html` component,
which actually renders the <picture> tag.

"""

from pathlib import Path
import re
from typing import Any, Literal

from jinja2 import pass_context
from jinja2.runtime import Context

from mosaic import page_types
from mosaic.images import get_picture_template_variables
from mosaic.text import assert_is_invariant_under_markdown

from .jinja_extensions import KwargsExtensionBase


__all__ = ["article_card_image", "render_picture", "PictureExtension"]


class PictureExtension(KwargsExtensionBase):
    """
    Defines the {% picture %} tag to render images.
    """

    tags = {"picture"}

    @pass_context
    def render_html(self, *args: Any, **kwargs: Any) -> str:
        """
        Render the picture tag.
        """
        html = render_picture(*args, **kwargs)
        assert_is_invariant_under_markdown(html)

        # Ensure there's a newline at the end of the rendered picture.
        #
        # This means the Mistune Markdown parser will see the picture as ended,
        # and not count the next paragraph as part of the HTML.
        return html + "\n"


def render_picture(
    context: Context,
    filename: str,
    width: int | str | None = None,
    height: int | str | None = None,
    parent: str | None = None,
    link_to: str | None = None,
    caller: Any | None = None,
    dst_prefix: str | Path | None = None,
    #
    # In the srcset and sizes attribute, should it be based on the width
    # of the output image or the pixel density?
    size_based_on: Literal["width", "density"] = "width",
    #
    # What's the max pixel density to support?
    max_pixel_density: int = 3,
    **kwargs: Any,
) -> str:
    """
    Create the HTML to display an image.
    """
    src_dir = context["src_dir"]
    out_dir = context["out_dir"]

    if isinstance(width, str):
        width = int(width)
    if isinstance(height, str):
        height = int(height)

    # Work out the source path to the image under `src/images`.
    #
    #   - If a picture tag sets an `parent`, use that
    #   - If the parent page has a date, look in the per-year folder
    #   - Otherwise, look in the `images` folder
    #
    images_dir = src_dir / "images"

    # TODO: Tidy up some of the `parent` handling logic?
    if parent is not None:
        src_path = src_dir / parent.lstrip("/") / filename
    else:
        if context["page"].date:
            src_path = images_dir / str(context["page"].date.year) / filename
        else:
            src_path = images_dir / filename

    template_variables = get_picture_template_variables(
        src_dir=src_dir,
        src_path=src_path,
        out_dir=out_dir,
        width=width,
        height=height,
        link_to=link_to,
        dst_prefix=dst_prefix,
        size_based_on=size_based_on,
        max_pixel_density=max_pixel_density,
        **kwargs,
    )

    # Render the <picture> tag.
    env = context.environment
    template = env.get_template("partials/picture.html")

    html: str = template.render(**template_variables)

    return html


@pass_context
def article_card_image(context: Context, article: page_types.Article) -> str:
    """
    Render an article card image.
    """
    # TODO: Handle alt sizes for article cards. Here's a comment from
    # the Jekyll code:
    #
    #    There are two breakpoints for cards:
    #
    #    * If the screen is 450px or narrower, there's only a single column
    #      of cards -- which take up almost all the screen width.
    #    * If the screen is 1000px or narrower, there are two columns of
    #      cards, each of which takes up about half the screen
    #    * If the screen is wider, there are three columns of cards,
    #      which all have a fixed width of ~300px
    #
    #    However, we expand the default width to 370px to handle tag pages
    #    which only have a small number of cards.
    #
    assert article.card_short_name is not None, (
        f"article has no associated card ({article})"
    )
    assert article.card_path is not None
    html = render_picture(
        context,
        filename=article.card_path.name,
        parent=str(article.card_path.parent),
        width=450,
        alt="",
        # e.g. /c/25
        dst_prefix=(
            Path("c") / str(article.date.year - 2000) / article.card_short_name
        ),
    )

    aspect_ratio = re.search(r"aspect-ratio: (?P<ratio>[0-9/]+)", html)
    assert aspect_ratio is not None
    if aspect_ratio.group("ratio") != "2":
        raise ValueError(
            f"expected 2/1 aspect ratio for sharing card {article.card_path.name}, "
            f"got {aspect_ratio}"
        )

    return html
