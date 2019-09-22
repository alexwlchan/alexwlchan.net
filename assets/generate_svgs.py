#!/usr/bin/env python
# -*- encoding: utf-8

import os
import pathlib
import subprocess
import sys

from lxml import etree
from jinja2 import Environment, FileSystemLoader


def find_svg_templates(search_root):
    for dirpath, _, filenames in os.walk(search_root):
        for f in filenames:
            if f.endswith(".svg.template"):
                yield pathlib.Path(os.path.join(search_root, dirpath, f))


def render_from_template(template_path):
    xml_str = get_rendered_xml(template_path)
    minified_xml_str = minify_xml(xml_str)

    root = subprocess.check_output([
        "git", "rev-parse", "--show-toplevel"]).decode("utf8").strip()

    # The asset directories are named YYYY-MM-{post_slug}, so we can work out
    # the year an asset belongs to by stripping off the first four characters.
    template_parent = template_path.resolve().parent.name
    year, *_ = template_parent.split("-")

    # We write to the src and the _site directory so we get nice fast previews
    # of the newly rendered SVGs.
    for images_dir in (
        pathlib.Path(root) / "src" / "_images" / year,
        pathlib.Path(root) / "_site" / "images" / year
    ):
        images_dir.mkdir(exist_ok=True)

        svg_path = images_dir / template_path.name.replace(".template", "")
        svg_path.write_bytes(minified_xml_str)


def get_rendered_xml(template_path):
    template_dir = template_path.parent

    # TODO: Drop the str() when https://github.com/pallets/jinja/pull/1064 is
    # merged and released.
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    # If you put a jinja_filters.py file inside the appropriate asset
    # directory, you can define any common variables or helpers you want
    # to be available to your templates.
    sys.path.append(str(template_dir))
    try:
        import jinja_filters
    except ImportError:
        pass
    else:
        for name in dir(jinja_filters):
            if not name.startswith("_"):
                env.filters[name] = getattr(jinja_filters, name)

    template = env.get_template(template_path.name)

    return template.render()


def minify_xml(xml_str):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.XML(xml_str, parser=parser)

    for comment in tree.xpath("//comment()"):
        parent = comment.parent()
        parent.remove(comment)

    return etree.tostring(tree)


if __name__ == "__main__":
    try:
        search_path = sys.argv[1]
    except IndexError:
        search_path = "."

    for svg_template_path in find_svg_templates(search_path):
        print(f"Rendering template at {svg_template_path.relative_to('.')}")
        render_from_template(svg_template_path)
