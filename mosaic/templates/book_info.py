from pathlib import Path

from jinja2 import Environment, pass_environment
from jinja2.parser import Parser
from jinja2.runtime import Context
from PIL import Image

from mosaic.models import CardConfig
from mosaic.pictures import create_image_derivatives
from .jinja_extensions import KwargsExtensionBase


class BookInfoExtension(KwargsExtensionBase):
    tags = {"book_info"}

    def parse(self, parser: Parser) -> str:
        return self._parse_kwargs(
            parser, tag_name="book_info", render_method="render_book_info"
        )

    @pass_environment
    def render_book_info(self, environment: Environment, **kwargs):
        template = environment.get_template("partials/book_info.html")
        return template.render(**kwargs)
