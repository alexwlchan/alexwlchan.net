"""
Tests for `mosaic.git.files`.
"""

from pathlib import Path

import pytest

from mosaic.git import GitFile


class TestGitFile:
    """
    Tests for `GitFile`.
    """

    @pytest.mark.parametrize(
        "path, label, contents",
        [
            ("README.md", "Markdown", "<empty>"),
            ("src/chives/media.py", "Python", "<empty>"),
            ("tests/stubs/smartypants.pyi", "Python type stub", "<empty>"),
            ("pyproject.toml", "TOML", "<empty>"),
            ("cassette.yml", "YAML", "<empty>"),
            ("requirements.txt", "pip requirements file", "<empty>"),
            ("dev_requirements.txt", "pip requirements file", "<empty>"),
            ("requirements.in", "pip-compile input file", "<empty>"),
            ("dev_requirements.in", "pip-compile input file", "<empty>"),
            ("unknown.bin", None, "<empty>"),
            ("create_thumbnail.rs", "Rust", "<empty>"),
            ("q.go", "Go", "<empty>"),
            (
                "info.plist",
                "XML property list",
                '<?xml version="1.0" encoding="UTF-8"?>',
            ),
        ],
    )
    def test_label(self, path: str, label: str | None, contents: str) -> None:
        """
        Tests for `GitFile.label`.
        """
        f = GitFile(path=Path(path), blob_id="123", size=0, is_binary=False)
        assert f.label(contents=contents) == label

    @pytest.mark.parametrize(
        "path, lang, contents",
        [
            ("README.md", "markdown", "<empty>"),
            ("src/chives/media.py", "python", "<empty>"),
            ("tests/stubs/smartypants.pyi", "python", "<empty>"),
            ("pyproject.toml", "toml", "<empty>"),
            ("cassette.yml", "yaml", "<empty>"),
            ("requirements.txt", "text", "<empty>"),
            ("unknown.bin", "text", "<empty>"),
            ("create_thumbnail.rs", "rust", "<empty>"),
            ("q.go", "go", "<empty>"),
            ("info.plist", "xml", '<?xml version="1.0" encoding="UTF-8"?>'),
        ],
    )
    def test_lang(self, path: str, lang: str, contents: str) -> None:
        """
        Tests for `GitFile.lang`.
        """
        f = GitFile(path=Path(path), blob_id="123", size=0, is_binary=False)
        assert f.lang(contents=contents) == lang

    def test_bash_script(self) -> None:
        """
        Check a bash script is recognised as such.
        """
        f = GitFile(path=Path("example.sh"), blob_id="123", size=0, is_binary=False)
        script_contents = "#!/usr/bin/env bash\necho 'hello world'"
        assert f.label(contents=script_contents) == "Bash"
        assert f.lang(contents=script_contents) == "bash"

        zsh_script_contents = "#!/usr/bin/env zsh\necho 'hello world'"
        assert f.label(contents=zsh_script_contents) is None
        assert f.lang(contents=zsh_script_contents) == "text"
