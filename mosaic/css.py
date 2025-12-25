from pathlib import Path
import re

from .models import Colours


def default_tint_colours(src_dir: Path) -> Colours:
    css_source = Path('css/variables.css').read_text()
    m_light = re.search(r'--default-primary-color-light:\s+(?P<colour>#[0-9a-f]{6});', css_source)
    m_dark = re.search(r'--default-primary-color-dark:\s+(?P<colour>#[0-9a-f]{6});', css_source)
    return Colours(
        css_light=m_light.group("colour"),
        css_dark = m_dark.group("colour")
    )
