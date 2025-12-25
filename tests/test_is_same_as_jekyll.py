from pathlib import Path

from mosaic.fs import list_paths


OLD_PATHS = set(list_paths("_site"))
NEW_PATHS = set(list_paths("_site.2"))


def test_sites_have_same_paths() -> None:
    """
    Both sites have the same paths.
    """
    old_paths = {p.relative_to(Path("_site")) for p in OLD_PATHS if p.suffix in {".html", ".xml"}}
    new_paths = {p.relative_to(Path("_site.2")) for p in NEW_PATHS if p.suffix in {".html", ".xml"}}
    assert old_paths == new_paths
