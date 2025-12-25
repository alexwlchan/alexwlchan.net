from pathlib import Path

from mosaic.pictures import create_image_derivatives
from mosaic.templates.pictures import render_picture


def test_creates_derivatives(tmp_path: Path) -> None:
    """
    Create some derivative images.
    """
    result, default_image = create_image_derivatives(
        src_path=Path("src/_images/367967055_7d1fbca99f_o.jpg"),
        src_dir=Path("src"),
        out_dir=tmp_path / "_site",
        desired_widths=[100, 200, 250],
        target_width=100,
    )

    assert result == {
        "image/avif": [
            "/images/367967055_7d1fbca99f_o_1x.avif 100w",
            "/images/367967055_7d1fbca99f_o_2x.avif 200w",
            "/images/367967055_7d1fbca99f_o_250w.avif 250w",
        ],
        "image/webp": [
            "/images/367967055_7d1fbca99f_o_1x.webp 100w",
            "/images/367967055_7d1fbca99f_o_2x.webp 200w",
            "/images/367967055_7d1fbca99f_o_250w.webp 250w",
        ],
        "image/jpeg": [
            "/images/367967055_7d1fbca99f_o_1x.jpg 100w",
            "/images/367967055_7d1fbca99f_o_2x.jpg 200w",
            "/images/367967055_7d1fbca99f_o_250w.jpg 250w",
        ],
    }
    assert default_image == "/images/367967055_7d1fbca99f_o_1x.jpg"
