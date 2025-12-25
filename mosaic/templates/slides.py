"""
The slide tag is for posts which are transcripts of talks.

It wraps the <picture> tag to insert a single slide.

Arguments:
    - filename: name of the slide image
    - alt: alt text for the slide
    - caption: the text to show below the figure (optional)

"""

from jinja2 import pass_context
from jinja2.parser import Parser
from jinja2.runtime import Context

from .pictures import render_picture
from .jinja_extensions import KwargsExtensionBase


class SlideExtension(KwargsExtensionBase):
    tags = {"slide"}

    def parse(self, parser: Parser) -> str:
        return self._parse_kwargs(
            parser, tag_name="slide", render_method="render_slide"
        )

    @pass_context
    def render_slide(
        self,
        context: Context,
        filename: str,
        caption: str | int = None,
        **kwargs,
    ):
        deck = context["page"].slug

        picture_tag = render_picture(
            context,
            filename=f"{deck}/{filename}",
            width=450,
            loading="lazy",
            link_to="original",
            **kwargs,
        )

        env = context.environment
        template = env.get_template("partials/slide.html")

        return template.render(picture_tag=picture_tag, caption=caption)
