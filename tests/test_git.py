"""
Tests for `mosaic.git`.
"""

from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tarfile
from typing import TypeAlias

import pytest

from mosaic.git import (
    ChangedBinaryFile,
    ChangedTextFile,
    ChangedTextFileHunk,
    Commit,
    CommitNotFoundError,
    Repository,
    TreeEntry,
)


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    """
    Returns the root of a temporary Git repository, which will only exist
    for the duration of a single test.
    """
    root = tmp_path / "repo"
    root.mkdir()
    return root


GitFn: TypeAlias = Callable[..., str]


@pytest.fixture
def git(repo_root: Path) -> GitFn:
    """
    Returns a wrapper function for running Git commands in the temp repo.
    """

    def inner(*args: str) -> str:
        output = subprocess.check_output(
            ["git"] + list(args),
            cwd=repo_root,
            env={"GIT_COMMITTER_DATE": "Mon 1 Jan 2001 01:01:01 GMT"},
            text=True,
        )
        return output.strip()

    inner("init", ".")
    inner("config", "user.name", "E. X. Ample")
    inner("config", "user.email", "me@example.com")

    return inner


@pytest.fixture
def repo(repo_root: Path, git: GitFn) -> Repository:
    """
    Returns an instance of `Repository` rooted in the temp repo.
    """
    return Repository(root=repo_root)


def test_history(git: GitFn, repo: Repository, repo_root: Path) -> None:
    """
    Test getting the history of a repository.
    """
    # Create a basic Git history:
    #
    #       "hello"
    #          ^
    #          |
    #    "hello world"
    #          ^
    #          |
    #   "bonjour monde"
    #
    (repo_root / "greeting.txt").write_text("hello")
    git("add", "greeting.txt")
    git("commit", "-m", "initial commit", "--date", "Sat 2 Feb 2002 02:02:02 GMT")

    (repo_root / "greeting.txt").write_text("hello world")
    git("add", "greeting.txt")
    git("commit", "-m", "add 'world'", "--date", "Mon 3 Mar 2003 03:03:03 GMT")

    (repo_root / "greeting.txt").write_text("bonjour monde")
    git("add", "greeting.txt")
    git("commit", "-m", "convert to French", "--date", "Sun 4 Apr 2004 04:04:04 GMT")

    assert repo.history() == [
        Commit(
            id="839cc3b6e949250e6e05aed6609834ec2493ac74",
            message="convert to French\n",
            author="E. X. Ample <me@example.com>",
            date=datetime(2004, 4, 4, 4, 4, 4, tzinfo=timezone.utc),
            parent_ids=["5e378f64de872be9e537331697e18a88ac2c9425"],
        ),
        Commit(
            id="5e378f64de872be9e537331697e18a88ac2c9425",
            message="add 'world'\n",
            author="E. X. Ample <me@example.com>",
            date=datetime(2003, 3, 3, 3, 3, 3, tzinfo=timezone.utc),
            parent_ids=["3ec2ee0a7c71e4b72faf7213c0e2a50b9477d37d"],
        ),
        Commit(
            id="3ec2ee0a7c71e4b72faf7213c0e2a50b9477d37d",
            message="initial commit\n",
            author="E. X. Ample <me@example.com>",
            date=datetime(2002, 2, 2, 2, 2, 2, tzinfo=timezone.utc),
            parent_ids=[],
        ),
    ]


class TestChangedFiles:
    """
    Tests for `changed_files`.
    """

    def test_initial_commit(
        self, git: GitFn, repo: Repository, repo_root: Path
    ) -> None:
        """
        Get the diff for an initial commit.
        """
        (repo_root / "greeting.txt").write_text("hello world\ntoday is monday\n")
        (repo_root / "cat.jpg").write_bytes(b"\x00\x01\x02\x03\x04\x05")
        git("add", "greeting.txt", "cat.jpg")
        git("commit", "-m", "initial commit")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert diff == [
            ChangedBinaryFile(
                old_path=None, new_path=Path("cat.jpg"), old_size=0, new_size=6
            ),
            ChangedTextFile(
                old_path=None,
                new_path=Path("greeting.txt"),
                old_size=0,
                new_size=28,
                lines_added=2,
                lines_deleted=0,
                hunks=[
                    ChangedTextFileHunk(
                        header="@@ -0,0 +1,2 @@",
                        lines=["+hello world\n", "+today is monday\n"],
                    )
                ],
            ),
        ]

    def test_add_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        An added file is a single `ChangedFile` where `old_path` is None.
        """
        (repo_root / "greeting.txt").write_text("hello world\n")
        git("add", "greeting.txt")
        git("commit", "-m", "initial commit")

        (repo_root / "added_text.txt").write_text("hello world\n")
        (repo_root / "added_binary.bin").write_bytes(b"\x00\x01\x02\x03\x04")
        git("add", "added_text.txt", "added_binary.bin")
        git("commit", "-m", "add two new files")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert diff == [
            ChangedBinaryFile(
                old_path=None, new_path=Path("added_binary.bin"), old_size=0, new_size=5
            ),
            ChangedTextFile(
                old_path=None,
                new_path=Path("added_text.txt"),
                old_size=0,
                new_size=12,
                lines_added=1,
                lines_deleted=0,
                hunks=[
                    ChangedTextFileHunk(
                        header="@@ -0,0 +1 @@", lines=["+hello world\n"]
                    )
                ],
            ),
        ]

    def test_delete_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        A deleted file is a `ChangedFile` where `new_path` is None.
        """
        (repo_root / "myfile.txt").write_text("hello world\n")
        (repo_root / "myfile.bin").write_bytes(b"\x00\x01\x02\x03\x04")
        git("add", "myfile.txt", "myfile.bin")
        git("commit", "-m", "initial commit")

        git("rm", "myfile.txt", "myfile.bin")
        git("commit", "-m", "delete both files")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert diff == [
            ChangedBinaryFile(
                old_path=Path("myfile.bin"), new_path=None, old_size=5, new_size=0
            ),
            ChangedTextFile(
                old_path=Path("myfile.txt"),
                new_path=None,
                old_size=12,
                new_size=0,
                lines_added=0,
                lines_deleted=1,
                hunks=[
                    ChangedTextFileHunk(
                        header="@@ -1 +0,0 @@", lines=["-hello world\n"]
                    )
                ],
            ),
        ]

    def test_modified_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        Test a modified file.
        """
        (repo_root / "myfile.txt").write_text("\n".join(f"{i}\n" for i in range(50)))
        (repo_root / "myfile.bin").write_bytes(b"\x00\x01\x02\x03\x04")
        git("add", "myfile.txt", "myfile.bin")
        git("commit", "-m", "initial commit")

        (repo_root / "myfile.txt").write_text(
            "\n".join(f"{i}\n" if i % 15 != 0 else "fizzbuzz" for i in range(50))
        )
        (repo_root / "myfile.bin").write_bytes(b"\x04\x03\x02\x01\x00")
        git("add", "myfile.txt", "myfile.bin")
        git("commit", "-m", "change both files")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert diff == [
            ChangedBinaryFile(
                old_path=Path("myfile.bin"),
                new_path=Path("myfile.bin"),
                old_size=5,
                new_size=5,
            ),
            ChangedTextFile(
                old_path=Path("myfile.txt"),
                new_path=Path("myfile.txt"),
                old_size=189,
                new_size=210,
                hunks=[
                    ChangedTextFileHunk(
                        header="@@ -1,5 +1,4 @@",
                        lines=["-0\n", "-\n", "+fizzbuzz\n", " 1\n", " \n", " 2\n"],
                    ),
                    ChangedTextFileHunk(
                        header="@@ -28,8 +27,7 @@",
                        lines=[
                            " \n",
                            " 14\n",
                            " \n",
                            "-15\n",
                            "-\n",
                            "+fizzbuzz\n",
                            " 16\n",
                            " \n",
                            " 17\n",
                        ],
                    ),
                    ChangedTextFileHunk(
                        header="@@ -58,8 +56,7 @@",
                        lines=[
                            " \n",
                            " 29\n",
                            " \n",
                            "-30\n",
                            "-\n",
                            "+fizzbuzz\n",
                            " 31\n",
                            " \n",
                            " 32\n",
                        ],
                    ),
                    ChangedTextFileHunk(
                        header="@@ -88,8 +85,7 @@",
                        lines=[
                            " \n",
                            " 44\n",
                            " \n",
                            "-45\n",
                            "-\n",
                            "+fizzbuzz\n",
                            " 46\n",
                            " \n",
                            " 47\n",
                        ],
                    ),
                ],
                lines_added=4,
                lines_deleted=8,
            ),
        ]

    def test_rename_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        Test renaming a file without changes.
        """
        (repo_root / "myfile.txt").write_text("\n".join(f"{i}\n" for i in range(50)))
        (repo_root / "myfile.bin").write_bytes(b"\x00\x01\x02\x03\x04")
        git("add", "myfile.txt", "myfile.bin")
        git("commit", "-m", "initial commit")

        git("mv", "myfile.txt", "mynewfile.txt")
        git("mv", "myfile.bin", "mynewfile.bin")
        git("commit", "-m", "rename both files")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert diff == [
            ChangedBinaryFile(
                old_path=Path("myfile.bin"),
                new_path=Path("mynewfile.bin"),
                old_size=5,
                new_size=5,
            ),
            ChangedTextFile(
                old_path=Path("myfile.txt"),
                new_path=Path("mynewfile.txt"),
                old_size=189,
                new_size=189,
                hunks=[],
                lines_added=0,
                lines_deleted=0,
            ),
        ]

    def test_rename_file_with_minor_chnages(
        self, git: GitFn, repo: Repository, repo_root: Path
    ) -> None:
        """
        Test renaming a file with minor changes.
        """
        (repo_root / "myfile.txt").write_text("\n".join(f"{i}\n" for i in range(50)))
        (repo_root / "myfile.bin").write_bytes(b"\x00\x01\x02\x03\x04" * 10)
        git("add", "myfile.txt", "myfile.bin")
        git("commit", "-m", "initial commit")

        (repo_root / "myfile.txt").write_text(
            "\n".join(f"{i}\n" if i != 42 else "the answer\n" for i in range(50))
        )
        (repo_root / "myfile.bin").write_bytes(b"\x00\x01\x02\x03\x04" * 9)
        git("mv", "myfile.txt", "mynewfile.txt")
        git("mv", "myfile.bin", "mynewfile.bin")
        git("add", "mynewfile.txt")
        git("add", "mynewfile.bin")

        git("commit", "-m", "rename and modify both files")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert diff == [
            ChangedBinaryFile(
                old_path=Path("myfile.bin"),
                new_path=Path("mynewfile.bin"),
                old_size=50,
                new_size=45,
            ),
            ChangedTextFile(
                old_path=Path("myfile.txt"),
                new_path=Path("mynewfile.txt"),
                old_size=189,
                new_size=197,
                hunks=[
                    ChangedTextFileHunk(
                        header="@@ -82,7 +82,7 @@",
                        lines=[
                            " \n",
                            " 41\n",
                            " \n",
                            "-42\n",
                            "+the answer\n",
                            " \n",
                            " 43\n",
                            " \n",
                        ],
                    )
                ],
                lines_added=1,
                lines_deleted=1,
            ),
        ]

    def test_nested_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        Paths are correct for nested files.
        """
        (repo_root / "1/2/3").mkdir(parents=True)
        (repo_root / "1/2/3/myfile.txt").write_text("hello world")
        git("add", "1/2/3/myfile.txt")
        git("commit", "-m", "initial commit")

        commit_id = git("rev-parse", "HEAD")
        diff = repo.changed_files(commit_id)

        assert len(diff) == 1
        assert diff[0].new_path == Path("1/2/3/myfile.txt")

    def test_bad_commit(self, repo: Repository) -> None:
        """
        Looking up the changed files of a non-existent commit is an error.
        """
        with pytest.raises(CommitNotFoundError):
            repo.changed_files(commit_id="123456890abcdef123456890abcdef123456890a")


class TestLookupName:
    """
    Tests for `lookup_name`.
    """

    def test_lookup_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        Look up a file at different commit IDs.
        """
        (repo_root / "greeting.txt").write_text("hello")
        git("add", "greeting.txt")
        git("commit", "-m", "initial commit")
        commit1 = git("rev-parse", "HEAD")

        (repo_root / "greeting.txt").write_text("hello world")
        git("add", "greeting.txt")
        git("commit", "-m", "add 'hello'")
        commit2 = git("rev-parse", "HEAD")

        assert repo.lookup_name(name="greeting.txt") == "hello world"
        assert repo.lookup_name(name="greeting.txt", commit_id=commit1) == "hello"
        assert repo.lookup_name(name="greeting.txt", commit_id=commit2) == "hello world"

        # Test with truncated Git IDs
        assert repo.lookup_name(name="greeting.txt", commit_id=commit1[:7]) == "hello"
        assert (
            repo.lookup_name(name="greeting.txt", commit_id=commit2[:7])
            == "hello world"
        )

    @pytest.mark.parametrize(
        "name, entries",
        [
            (
                ".",
                {
                    TreeEntry(type="folder", name="1"),
                    TreeEntry(type="folder", name="2"),
                    TreeEntry(type="file", name="numbers.txt"),
                },
            ),
            (
                "1",
                {
                    TreeEntry(type="folder", name="1a"),
                    TreeEntry(type="file", name="eins.txt"),
                },
            ),
            (
                "1/1a",
                {
                    TreeEntry(type="folder", name="1a1"),
                    TreeEntry(type="folder", name="1a2"),
                },
            ),
            ("1/1a/1a1", {TreeEntry(type="file", name="uno.txt")}),
            ("2", {TreeEntry(type="file", name="dos.txt")}),
        ],
    )
    def test_lookup_directory(
        self,
        git: GitFn,
        repo: Repository,
        repo_root: Path,
        name: str,
        entries: set[TreeEntry],
    ) -> None:
        """
        Look up a directory at different points.
        """
        for name_to_write in [
            "numbers.txt",
            "1/1a/1a1/uno.txt",
            "1/1a/1a2/one.txt",
            "1/eins.txt",
            "2/dos.txt",
        ]:
            p = repo_root / name_to_write
            p.parent.mkdir(exist_ok=True, parents=True)
            p.write_text("hello world\n")
            git("add", p)

        git("commit", "-m", "initial commit")

        assert repo.lookup_name(name) == entries

    def test_missing_file(self, git: GitFn, repo: Repository, repo_root: Path) -> None:
        """
        Looking up a non-existent file/directory is an error.
        """
        (repo_root / "greeting.txt").write_text("hello world")
        git("add", "greeting.txt")
        git("commit", "-m", "initial commit")

        with pytest.raises(FileNotFoundError):
            repo.lookup_name(name="README.md")

    def test_bad_reference(self, repo: Repository) -> None:
        """
        Looking up a non-existent commit is an error.
        """
        with pytest.raises(CommitNotFoundError):
            repo.lookup_name(
                name="README.md", commit_id="123456890abcdef123456890abcdef123456890a"
            )


def test_create_archive(
    git: GitFn, repo: Repository, repo_root: Path, tmp_path: Path
) -> None:
    """
    Create a tar.gz archive with the `create_archive` function.
    """
    (repo_root / "greeting.txt").write_text("hello world")
    git("add", "greeting.txt")

    (repo_root / "1/2/3").mkdir(parents=True)
    (repo_root / "1/2/3/nested.txt").write_text("this is a nested file")
    git("add", "1/2/3/nested.txt")

    git("commit", "-m", "initial commit")

    for _ in range(3):
        out_path = repo.create_archive(folder=tmp_path / "out")
        assert out_path.exists()

        with tarfile.open(out_path) as tf:
            assert set(tf.getnames()) == {"1/2/3/nested.txt", "greeting.txt"}

            f = tf.extractfile("greeting.txt")
            assert f is not None
            assert f.read() == b"hello world"
