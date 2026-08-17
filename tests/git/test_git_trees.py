"""
Tests for `mosaic.git.trees`.
"""

from collections.abc import Callable
from collections import OrderedDict
from pathlib import Path
from typing import TypeAlias


from mosaic.git import GitFile, GitRepository, NavigableFile, NavigableTree


GitFn: TypeAlias = Callable[..., None]


def test_git_tree(git: GitFn, repo_root: Path) -> None:
    """
    Test constructing the working directory tree for a repo.
    """
    for path in (
        "greeting.txt",
        "numbers/1/uno.txt",
        "numbers/1/eins.txt",
        "numbers/2/duo.txt",
        "colours/red.txt",
    ):
        (repo_root / path).parent.mkdir(exist_ok=True, parents=True)
        (repo_root / path).write_text(f"this file is {path}")
        git("add", path)

    (repo_root / "zero.bin").write_bytes(b"\x00" * 1024)
    git("add", "zero.bin")

    git("commit", "-m", "initial commit")

    repo = GitRepository(
        name="example", description="example repo", repo_root=repo_root
    )

    assert sorted(repo.tree.files, key=lambda f: str(f.path)) == [
        GitFile(
            path=Path("colours/red.txt"),
            blob_id="ee93f5fc4904a140e94a0c5123c4280cbde72ea1",
            size=28,
            is_binary=False,
        ),
        GitFile(
            path=Path("greeting.txt"),
            blob_id="e94ba47db730b7ba94f32d51be06645c7cbc2a74",
            size=25,
            is_binary=False,
        ),
        GitFile(
            path=Path("numbers/1/eins.txt"),
            blob_id="837e6cf1c66dd116e2a77512802df816a859884a",
            size=31,
            is_binary=False,
        ),
        GitFile(
            path=Path("numbers/1/uno.txt"),
            blob_id="51cdd03392f4a1b7175044fa9932fc98fe05fc3f",
            size=30,
            is_binary=False,
        ),
        GitFile(
            path=Path("numbers/2/duo.txt"),
            blob_id="2cd6ba5db484b1e12a8d674f6a35a001e7771f9d",
            size=30,
            is_binary=False,
        ),
        GitFile(
            path=Path("zero.bin"),
            blob_id="06d7405020018ddf3cacee90fd4af10487da3d20",
            size=1024,
            is_binary=True,
        ),
    ]
    assert repo.navigable_tree.files == [
        NavigableFile(name="greeting.txt"),
        NavigableFile(name="zero.bin", is_binary=True),
    ]

    assert (
        repo.get_blob_data("2cd6ba5db484b1e12a8d674f6a35a001e7771f9d")
        == b"this file is numbers/2/duo.txt"
    )


def test_navigable_tree_from_paths() -> None:
    """
    Test that `NavigableTree.from_paths` constructs a tree correctly.
    """
    paths = [
        "greeting.txt",
        "README.md",
        "numbers/1/uno.txt",
        "numbers/1/eins.txt",
        "numbers/2/duo.txt",
        "colours/red.txt",
        "quadrilaterals/squares/1-1-1-1.txt",
        "quadrilaterals/squares/2-2-2-2.txt",
        "quadrilaterals/squares/3-3-3-3.txt",
        "shapes/triangles/pythagoras/3-4-5.txt",
        "shapes/triangles/pythagoras/5-12-13.txt",
        "shapes/triangles/pythagoras/8-15-17.txt",
        "tests/test_shapes.py",
    ]

    tree = NavigableTree.from_files(
        [GitFile(path=Path(p), size=0, is_binary=False, blob_id="XXX") for p in paths]
    )

    def navigable_files(*names: str) -> list[NavigableFile]:
        return [NavigableFile(name=n) for n in names]

    assert tree == NavigableTree(
        folders=OrderedDict(
            [
                (Path("colours"), NavigableTree(files=navigable_files("red.txt"))),
                (
                    Path("numbers"),
                    NavigableTree(
                        folders=OrderedDict(
                            [
                                (
                                    Path("1"),
                                    NavigableTree(
                                        files=navigable_files("eins.txt", "uno.txt")
                                    ),
                                ),
                                (
                                    Path("2"),
                                    NavigableTree(files=navigable_files("duo.txt")),
                                ),
                            ]
                        )
                    ),
                ),
                (
                    Path("quadrilaterals/squares"),
                    NavigableTree(
                        files=navigable_files(
                            "1-1-1-1.txt", "2-2-2-2.txt", "3-3-3-3.txt"
                        )
                    ),
                ),
                (
                    Path("shapes/triangles/pythagoras"),
                    NavigableTree(
                        files=navigable_files("3-4-5.txt", "5-12-13.txt", "8-15-17.txt")
                    ),
                ),
                (
                    Path("tests"),
                    NavigableTree(files=navigable_files("test_shapes.py")),
                ),
            ]
        ),
        files=navigable_files("README.md", "greeting.txt"),
    )
