"""
Tests for mosaic.
"""

import glob
from pathlib import Path

from mosaic import Site


def test_build_base_css_file(tmp_path: Path) -> None:
    """
    Tests for `build_base_css_file`.
    """
    # Generate a new CSS file
    out_dir = tmp_path / "_out"
    s = Site(css_path=Path("css/style.css"), src_dir=Path("src"), out_dir=out_dir)
    s.build_base_css_file()

    assert len(glob.glob(f"{out_dir}/static/style.*.css")) == 1

    # Check it starts with `:root`, which is the variable declaration
    # at the top of my CSS file.
    css_path = glob.glob(f"{out_dir}/static/style.*.css")[0]
    with open(css_path) as in_file:
        css = in_file.read()
    assert css.startswith(":root")

    # Write a new CSS file into that directory, as if from an old process
    # with different CSS.
    #
    # Check it gets deleted.
    (out_dir / "static/style.123.css").write_text("old_css")
    s.build_base_css_file()

    assert len(glob.glob(f"{out_dir}/static/style.*.css")) == 1
