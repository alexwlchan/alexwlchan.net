"""
Model to describe a single file in a Git repository.
"""

from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel


__all__ = ["GitFile"]


@dataclass(frozen=True)
class LanguageSpec:
    """
    Describes the label and Pygments lexer for a specific file.
    """

    label: str
    lexer: str


FILE_TYPES: dict[str, LanguageSpec] = {
    ".css": LanguageSpec("CSS", "css"),
    ".fish": LanguageSpec("Fish shell", "fish"),
    ".go": LanguageSpec("Go", "go"),
    ".html": LanguageSpec("HTML", "html"),
    ".js": LanguageSpec("JavaScript", "javascript"),
    ".json": LanguageSpec("JSON", "json"),
    ".md": LanguageSpec("Markdown", "markdown"),
    ".py": LanguageSpec("Python", "python"),
    ".pyi": LanguageSpec("Python type stub", "python"),
    ".rs": LanguageSpec("Rust", "rust"),
    ".svg": LanguageSpec("SVG", "xml"),
    ".swift": LanguageSpec("Swift", "swift"),
    ".toml": LanguageSpec("TOML", "toml"),
    ".txt": LanguageSpec("Plain text", "text"),
    ".yml": LanguageSpec("YAML", "yaml"),
}

SHEBANG_TYPES: dict[str, LanguageSpec] = {
    "#!/usr/bin/env bash": LanguageSpec("Bash", "bash"),
    "#!/usr/bin/env osascript": LanguageSpec("AppleScript", "applescript"),
    "#!/usr/bin/env osascript -l JavaScript": LanguageSpec(
        "JXA (JavaScript for Automation)", "javascript"
    ),
    "#!/usr/bin/env python": LanguageSpec("Python", "python"),
    "#!/usr/bin/env python3": LanguageSpec("Python", "python"),
    "#!/usr/bin/env swift": LanguageSpec("Swift", "swift"),
}


class GitFile(BaseModel):
    """
    GitFile describes a single file inside a Git repository.
    """

    # Path of this file within the working directory
    path: Path

    # The ID of the blob object with the contents of this file
    blob_id: str

    # The size of the file in bytes
    size: int

    # Whether this is a binary file
    is_binary: bool

    def _resolve_spec(self, contents: str) -> LanguageSpec | None:
        """
        Resolve file type metadata based on extension or shebang.
        """
        if self.path.name.endswith("requirements.txt"):
            return LanguageSpec("pip requirements file", "text")

        if self.path.name.endswith("requirements.in"):
            return LanguageSpec("pip-compile input file", "text")

        if spec := FILE_TYPES.get(self.path.suffix):
            return spec

        if self.path.suffix == ".plist" and contents.startswith("<?xml"):
            return LanguageSpec("XML property list", "xml")

        try:
            first_line = contents.splitlines()[0].rstrip()
            if spec := SHEBANG_TYPES.get(first_line):
                return spec
        except IndexError:
            pass

        return None

    def label(self, contents: str) -> str | None:
        """
        Return a human-readable label describing the type of this file.
        """
        if spec := self._resolve_spec(contents):
            return spec.label

        return None

    def lang(self, contents: str) -> str:
        """
        Return a Pygments lexer shortname for this file.
        """
        if spec := self._resolve_spec(contents):
            return spec.lexer

        return "text"
