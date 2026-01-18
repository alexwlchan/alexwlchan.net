"""
Shared test fixtures and helpers.
"""

from pathlib import Path

from jinja2 import Environment
import pytest

from mosaic import templates as t


@pytest.fixture
def src_dir(tmp_path: Path) -> Path:
    """
    Returns a source directory for the site.
    """
    return tmp_path / "src"


@pytest.fixture
def out_dir(tmp_path: Path) -> Path:
    """
    Returns an output directory for the site.
    """
    return tmp_path / "out"


@pytest.fixture
def env(src_dir: Path, out_dir: Path) -> Environment:
    """
    Creates a basic instance of the Jinja2 environment.
    """
    return t.get_jinja_environment(src_dir, out_dir)
