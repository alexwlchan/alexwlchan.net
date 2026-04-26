"""
Tests for `mosaic.git`.
"""

from collections.abc import Callable
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import time
from typing import TypeAlias

import pygit2
import pytest

from mosaic.git import (
    ChangedFile,
    Commit,
    GitFile,
    GitRepository,
    NavigableFile,
    NavigableTree,
    Stats,
    sort_tags,
)


GitFn: TypeAlias = Callable[..., None]


class TestGitRepository:
    """
    Tests for `GitRepository`.
    """

    def test_head(self, repo: GitRepository) -> None:
        """
        The HEAD points to the hex ID of the most recent commit.
        """
        assert repo.head == "cb82565da2bff937855a0c53845e2dc98c58dfeb"

    def test_archive(self, repo: GitRepository, out_dir: Path) -> None:
        """
        The tar.gz archive contains the files from the current HEAD.
        """
        # Create an archive, then check the output with the `tar` command.
        #
        # I'm deliberately not using tarfile, so I check the archive with
        # a different tool than the one used to create it.
        archive_path = repo.write_archive(out_dir)
        assert (
            archive_path
            == out_dir / "example-cb82565da2bff937855a0c53845e2dc98c58dfeb.tar.gz"
        )
        tar_output = subprocess.check_output(
            ["tar", "tvf", str(archive_path)], text=True
        )
        tar_filenames = {line.split()[-1] for line in tar_output.splitlines()}
        assert tar_filenames == {"README.md", "greeting.en.txt", "greeting.fr.txt"}

    def test_archive_is_only_latest(
        self, git: GitFn, repo_root: Path, out_dir: Path
    ) -> None:
        """
        The output directory only has the latest archive.
        """
        # Create an initial commit
        (repo_root / "README.md").write_text("creating the README")
        git("add", "README.md")
        git("commit", "-m", "initial commit")

        # Write the archive twice, and check the paths are consistent
        repo1 = GitRepository(
            name="example", description="an example repo", repo_root=repo_root
        )
        archive_path1 = repo1.write_archive(out_dir)
        assert archive_path1.exists()
        assert archive_path1 == repo1.write_archive(out_dir)

        # Change a file in the Git repo.
        (repo_root / "README.md").write_text("updating the README")
        git("add", "README.md")
        git("commit", "-m", "updating the README")

        # Create a new archive, and check the archive path has changed,
        # and the old archive has been cleaned up.
        repo2 = GitRepository(
            name="example", description="an example repo", repo_root=repo_root
        )
        archive_path2 = repo2.write_archive(out_dir)

        assert archive_path2.exists()
        assert archive_path1 != archive_path2
        assert not archive_path1.exists()

        # Check that creating archives for different repos are independent.
        repo3 = GitRepository(
            name="different", description="a different repo", repo_root=repo_root
        )
        archive_path3 = repo3.write_archive(out_dir)

        assert archive_path2.exists()
        assert archive_path3.exists()
        assert archive_path2 != archive_path3

    def test_last_updated(self, repo: GitRepository) -> None:
        """
        The last updated date is the date of the first commit.
        """
        assert repo.last_updated == datetime(2005, 5, 5, 5, 5, 5, tzinfo=timezone.utc)

    def test_commits(self, repo: GitRepository) -> None:
        """
        The commits are correct.
        """
        print(repo.commits)
        assert repo.commits == OrderedDict(
            {
                "cb82565da2bff937855a0c53845e2dc98c58dfeb": Commit(
                    id="cb82565da2bff937855a0c53845e2dc98c58dfeb",
                    message="add a README file",
                    author="E. X. Ample <me@example.com>",
                    date=datetime(2005, 5, 5, 5, 5, 5, tzinfo=timezone.utc),
                    parent_ids=["85ea442996d28dbac757d7080071ab20222fd76d"],
                    changed_files=[
                        ChangedFile(
                            old_path=Path("README.md"),
                            new_path=Path("README.md"),
                            new_size=23,
                            old_size=0,
                            stats=Stats(additions=1, deletions=0),
                            diff_text=(
                                "diff --git a/README.md b/README.md\n"
                                "new file mode 100644\n"
                                "index 0000000..846c00b\n"
                                "--- /dev/null\n"
                                "+++ b/README.md\n"
                                "@@ -0,0 +1 @@\n"
                                "+this is an example repo\n"
                                "\\ No newline at end of file\n"
                            ),
                        )
                    ],
                ),
                "85ea442996d28dbac757d7080071ab20222fd76d": Commit(
                    id="85ea442996d28dbac757d7080071ab20222fd76d",
                    message="convert to French",
                    author="E. X. Ample <me@example.com>",
                    date=datetime(2004, 4, 4, 4, 4, 4, tzinfo=timezone.utc),
                    parent_ids=["200cffd1814043a79dcc1dc334b9577a5b753cac"],
                    changed_files=[
                        ChangedFile(
                            old_path=Path("greeting.fr.txt"),
                            new_path=Path("greeting.fr.txt"),
                            new_size=13,
                            old_size=0,
                            stats=Stats(additions=1, deletions=0),
                            diff_text=(
                                "diff --git a/greeting.fr.txt b/greeting.fr.txt\n"
                                "new file mode 100644\n"
                                "index 0000000..b452305\n"
                                "--- /dev/null\n"
                                "+++ b/greeting.fr.txt\n"
                                "@@ -0,0 +1 @@\n+bonjour monde\n"
                                "\\ No newline at end of file\n"
                            ),
                        )
                    ],
                ),
                "200cffd1814043a79dcc1dc334b9577a5b753cac": Commit(
                    id="200cffd1814043a79dcc1dc334b9577a5b753cac",
                    message="add 'world'",
                    author="E. X. Ample <me@example.com>",
                    date=datetime(2003, 3, 3, 3, 3, 3, tzinfo=timezone.utc),
                    parent_ids=["e90e5a42bd2c3b69a5abf7155bb5a3031523c5b2"],
                    changed_files=[
                        ChangedFile(
                            old_path=Path("greeting.en.txt"),
                            new_path=Path("greeting.en.txt"),
                            new_size=11,
                            old_size=5,
                            stats=Stats(additions=1, deletions=1),
                            diff_text=(
                                "diff --git a/greeting.en.txt b/greeting.en.txt\n"
                                "index b6fc4c6..95d09f2 100644\n"
                                "--- a/greeting.en.txt\n"
                                "+++ b/greeting.en.txt\n"
                                "@@ -1 +1 @@\n"
                                "-hello\n"
                                "\\ No newline at end of file\n"
                                "+hello world\n"
                                "\\ No newline at end of file\n"
                            ),
                        )
                    ],
                ),
                "e90e5a42bd2c3b69a5abf7155bb5a3031523c5b2": Commit(
                    id="e90e5a42bd2c3b69a5abf7155bb5a3031523c5b2",
                    message="initial commit",
                    author="E. X. Ample <me@example.com>",
                    date=datetime(2002, 2, 2, 2, 2, 2, tzinfo=timezone.utc),
                    parent_ids=[],
                    changed_files=[
                        ChangedFile(
                            old_path=Path("greeting.en.txt"),
                            new_path=Path("greeting.en.txt"),
                            new_size=5,
                            old_size=0,
                            stats=Stats(additions=1, deletions=0),
                            diff_text=(
                                "diff --git a/greeting.en.txt b/greeting.en.txt\n"
                                "new file mode 100644\n"
                                "index 0000000..b6fc4c6\n"
                                "--- /dev/null\n"
                                "+++ b/greeting.en.txt\n"
                                "@@ -0,0 +1 @@\n"
                                "+hello\n"
                                "\\ No newline at end of file\n"
                            ),
                        )
                    ],
                ),
            }
        )

    def test_tags(self, repo: GitRepository) -> None:
        """
        The tags are sorted in human-readable order.
        """
        assert repo.tags == OrderedDict(
            [
                ("v10", "85ea442996d28dbac757d7080071ab20222fd76d"),
                ("v2", "200cffd1814043a79dcc1dc334b9577a5b753cac"),
                ("v1", "e90e5a42bd2c3b69a5abf7155bb5a3031523c5b2"),
            ]
        )

    def test_clone(self, repo: GitRepository, tmp_path: Path) -> None:
        """
        The cloned repository can be cloned over HTTP.
        """
        clone_dir = tmp_path / "example.git"
        repo.create_clone_for_serving(out_dir=clone_dir)

        cmd = ["python3", "-m", "http.server", "8123", "--directory", str(tmp_path)]
        proc = subprocess.Popen(cmd)

        # Sleep for 1 second to give the server time to wake up and start
        # serving the directory. This isn't a great way to write tests, but
        # the rest of the test suite is fast enough and this avoids flakiness
        # when running tests in parallel.
        time.sleep(1)

        try:
            subprocess.check_call(
                [
                    "git",
                    "clone",
                    "http://localhost:8123/example.git",
                    str(tmp_path / "cloned_over_http.git"),
                ]
            )
            subprocess.check_call(["git", "log"], cwd=tmp_path / "cloned_over_http.git")
        finally:
            proc.terminate()
            proc.wait()


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


@pytest.mark.parametrize(
    "stats, stats_str",
    [
        (Stats(additions=33, deletions=24), "+33, &minus;24"),
        (Stats(additions=0, deletions=24), "&minus;24"),
        (Stats(additions=33, deletions=0), "+33"),
    ],
)
def test_stats_str(stats: Stats, stats_str: str) -> None:
    """
    Check the human-readable representation of `Stats`.
    """
    assert str(stats) == stats_str


def test_commit_stats() -> None:
    """
    The stats for a commit count all the additions and deletions
    for every file changed in the commit.
    """
    repo = pygit2.Repository(Path.home() / "repos/chives")

    commit = repo.get("aac432816394a98e493703ee814f7a8fec2390b2")
    assert isinstance(commit, pygit2.Commit)

    _, parsed_commit = Commit.from_pygit2_commit(repo, commit)

    assert parsed_commit.stats == Stats(additions=70, deletions=16)


def test_commit_summary() -> None:
    """
    The summary of a commit is the first line of a commit message.
    """
    repo = pygit2.Repository(Path.home() / "repos/chives")

    commit = repo.get("7fd9cd0d5c06b7b0480642bca194229a1a084ab8")
    assert isinstance(commit, pygit2.Commit)

    _, parsed_commit = Commit.from_pygit2_commit(repo, commit)

    assert (
        parsed_commit.summary == "all: remove the silver-nitrate and httpx dependencies"
    )
    assert parsed_commit.message == (
        "all: remove the silver-nitrate and httpx dependencies\n"
        "\n"
        "silver-nitrate is a library I wrote while working at the Flickr Foundation,\n"
        "but they're slowing down and it's unclear if the library will still be\n"
        "maintained: https://www.flickr.org/looking-ahead-simplifying-our-strategy/\n"
        "I wrote all this code, so just copy it into this project.\n"
        "\n"
        "It's unclear if httpx is still maintained, so replace it with standard\n"
        "library. See https://tildeweb.nl/~michiel/httpxyz.html"
    )


@pytest.mark.parametrize(
    "tags, sorted_tags",
    [
        ([], []),
        (["v1", "v3", "v2"], ["v3", "v2", "v1"]),
        (["v1", "v2", "fish"], ["v1", "v2", "fish"]),
    ],
)
def test_sort_tags(tags: list[str], sorted_tags: list[str]) -> None:
    """
    Tests for `sort_tags`.
    """
    input = OrderedDict([(t, "<commit>") for t in tags])
    output = sort_tags(input)
    assert list(output.keys()) == sorted_tags


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
                                    "1",
                                    NavigableTree(
                                        files=navigable_files("eins.txt", "uno.txt")
                                    ),
                                ),
                                (
                                    "2",
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


def test_readme_contents(git: GitFn, repo_root: Path, tmp_path: Path) -> None:
    """
    The `readme_contents()` method returns the most recent version
    of the README.md file.
    """
    for i in range(1, 10):
        (repo_root / "README.md").write_text(f"This is version {i} of the README")
        git("add", "README.md")
        git("commit", "-m", "update README")

    repo = GitRepository(
        name="example", description="example repo", repo_root=repo_root
    )

    assert repo.readme_contents() == "This is version 9 of the README"


class TestGitFile:
    """
    Tests for `GitFile`.
    """

    @pytest.mark.parametrize(
        "path, label",
        [
            ("README.md", "Markdown"),
            ("src/chives/media.py", "Python"),
            ("tests/stubs/smartypants.pyi", "Python type stub"),
            ("pyproject.toml", "TOML"),
            ("cassette.yml", "YAML"),
            ("requirements.txt", "pip requirements file"),
            ("dev_requirements.txt", "pip requirements file"),
            ("requirements.in", "pip-compile input file"),
            ("dev_requirements.in", "pip-compile input file"),
            ("unknown.bin", None),
            ("create_thumbnail.rs", "Rust"),
        ],
    )
    def test_label(self, path: str, label: str | None) -> None:
        """
        Tests for `GitFile.label`.
        """
        f = GitFile(path=Path(path), blob_id="123", size=0, is_binary=False)
        assert f.label == label

    @pytest.mark.parametrize(
        "path, lang",
        [
            ("README.md", "markdown"),
            ("src/chives/media.py", "python"),
            ("tests/stubs/smartypants.pyi", "python"),
            ("pyproject.toml", "toml"),
            ("cassette.yml", "yaml"),
            ("requirements.txt", "text"),
            ("unknown.bin", "text"),
            ("create_thumbnail.rs", "rust"),
        ],
    )
    def test_lang(self, path: str, lang: str) -> None:
        """
        Tests for `GitFile.lang`.
        """
        f = GitFile(path=Path(path), blob_id="123", size=0, is_binary=False)
        assert f.lang == lang
