import base64
from datetime import datetime
import glob
from io import BytesIO
import json
from pathlib import Path

from jinja2 import Environment, nodes, pass_environment
from jinja2.ext import Extension
from jinja2.runtime import Context
from PIL import Image

from .pictures import render_picture
from .text import markdownify


class UpdateExtension(Extension):
    tags = {"update"}

    def parse(self, parser):
        # The first token should be the name of the tag, i.e. "update"
        first_token = next(parser.stream)

        # Parse the next expression (the date of the update)
        date_updated = parser.parse_expression()

        # Parse everything until we hit '{% endupdate %}'
        # 'drop_needle=True' tells Jinja to remove the 'endupdate' token
        # from the stream
        body = parser.parse_statements(["name:endupdate"], drop_needle=True)

        kwargs = [nodes.Keyword("date_updated", date_updated)]

        return nodes.CallBlock(
            self.call_method("render_update", kwargs=kwargs), [], [], body
        ).set_lineno(first_token.lineno)

    @pass_environment
    def render_update(self, environment: Environment, date_updated: str, caller) -> str:
        content = caller()
        date_updated = datetime.strptime(date_updated, "%Y-%m-%d")

        timestamp_tpl = environment.get_template("partials/timestamp.html")
        timestamp_html = timestamp_tpl.render(date=date_updated)

        md = f"**Update, {timestamp_html}:** {content}"

        update_tpl = environment.get_template("partials/update.html")
        return update_tpl.render(date=date_updated, text=markdownify(md))
