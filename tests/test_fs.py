"""
Tests for `mosaic.fs`.
"""

from pathlib import Path

import pytest

from mosaic.fs import find_paths_under


class TestFindPathsUnder:
    """
    Tests for `find_paths_under`.
    """

    def test_cannot_get_files_under_file(self) -> None:
        """
        Trying to look for files under a file, not a folder, is an error.
        """
        root = Path(__file__)

        with pytest.raises(ValueError, match="Cannot find files under non-directory"):
            next(find_paths_under(root))

    def test_cannot_get_files_under_non_existent_dir(self) -> None:
        """
        Finding files under a non-existent directory returns an empty list.
        """
        root = Path("does_not_exist/")

        with pytest.raises(FileNotFoundError):
            next(find_paths_under(root))

    def test_finds_matching_files(self, tmp_path: Path) -> None:
        """
        Find files that exist.
        """
        (tmp_path / "greeting.txt").write_text("hello world")

        paths = [tmp_path / "greeting.txt"]

        assert list(find_paths_under(tmp_path)) == paths
        assert list(find_paths_under(tmp_path, suffix=".txt")) == paths
        assert list(find_paths_under(tmp_path, suffix=".TXT")) == paths

        assert list(find_paths_under(tmp_path, suffix=".html")) == []
