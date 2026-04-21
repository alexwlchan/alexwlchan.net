"""
Functions for interacting with Git.
"""

from collections import OrderedDict
from collections.abc import Iterable
import codecs
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
from typing import Self
import uuid

from pydantic import BaseModel
import pygit2
from pygit2.enums import ReferenceFilter, SortMode


__all__ = ["git_root"]


def as_hex(oid: pygit2.Oid) -> str:
    """
    Convert a Git object ID to a human-readable hex string.
    """
    return codecs.encode(oid.raw, "hex").decode("ascii")


def git_root() -> Path:
    """
    Return the root of the current Git checkout.

    This expects to be run in a non-bare checkout, and returns the root
    of the checkout -- so `.git` is a subdirectory.
    """
    p = pygit2.discover_repository(Path.cwd())
    assert p is not None
    git_dir = Path(p)
    assert git_dir.name == ".git"
    return git_dir.parent


class Stats(BaseModel):
    """
    Stats about a diff, either per-file or per-commit.
    """

    additions: int
    deletions: int

    def __str__(self) -> str:
        assert self.additions > 0 or self.deletions > 0
        if self.additions and self.deletions:
            return f"+{self.additions}, &minus;{self.deletions}"
        elif self.additions:
            return f"+{self.additions}"
        else:
            return f"&minus;{self.deletions}"


class ChangedFile(BaseModel):
    """
    A single changed file in a commit.
    """

    old_path: Path
    new_path: Path

    new_size: int
    old_size: int

    stats: Stats
    diff_text: str

    # TODO(2026-04-16): What about binary files?

    @classmethod
    def from_pygit2_patch(cls, patch: pygit2.Patch) -> "ChangedFile":
        """
        Create a `Patch` from the pygit2 data structures.
        """
        # Note(2026-04-16): The type signature for `text` says it can be `None`,
        # but I've never seen that in practice.
        #
        # For now, assert that `text` is always defined, and I'll handle it if
        # I ever have a real example to test with.
        #
        # TODO(2026-04-16): Use `diff.hunks` to get this text without the
        # header on top.
        diff_text = patch.text
        assert isinstance(diff_text, str), (
            f"Got empty `text` attribute on patch (data={patch.data!r})"
        )

        return ChangedFile(
            old_path=Path(patch.delta.old_file.path),
            new_path=Path(patch.delta.new_file.path),
            old_size=patch.delta.old_file.size,
            new_size=patch.delta.new_file.size,
            stats=Stats(
                additions=patch.line_stats[1],
                deletions=patch.line_stats[2],
            ),
            diff_text=diff_text,
        )


class Commit(BaseModel):
    """
    Information about a single commit.
    """

    id: str
    message: str
    author: str
    date: datetime
    parent_ids: list[str]
    changed_files: list[ChangedFile]

    @property
    def summary(self) -> str:
        """
        The first line of the commit message.
        """
        return self.message.splitlines()[0]

    @classmethod
    def from_pygit2_commit(
        cls, repo: pygit2.Repository, commit: pygit2.Commit
    ) -> tuple[str, "Commit"]:
        """
        Create a `Commit` from the pygit2 data structures.
        """
        parent = commit.parents[0] if commit.parents else None
        if parent is None:
            diff = commit.tree.diff_to_tree(swap=True)
        else:
            diff = repo.diff(parent, commit)

        # Note(2026-04-16): The type signature for the __iter__ method
        # says it returns `Patch | None`, but I've never seen an instance
        # of it returning None. I don't know when that would occur.
        #
        # For now, assert that all patches are defined, and I'll handle
        # it if I ever have a real example to test with.
        patches: list[pygit2.Patch] = [patch for patch in diff if patch]
        assert len(patches) == len(list(diff)), (
            f"Got some empty patches for commit {commit.id}: {list(diff)}"
        )

        changed_files = [ChangedFile.from_pygit2_patch(patch) for patch in patches]

        commit_id = as_hex(commit.id)

        return commit_id, Commit(
            id=commit_id,
            message=commit.message.strip(),
            author=f"{commit.author.name} <{commit.author.email}>",
            date=datetime.fromtimestamp(commit.author.time, tz=timezone.utc),
            parent_ids=[as_hex(p) for p in commit.parent_ids],
            changed_files=changed_files,
        )

    @property
    def stats(self) -> Stats:
        """
        Overall stats for the commit.
        """
        additions = sum(cf.stats.additions for cf in self.changed_files)
        deletions = sum(cf.stats.deletions for cf in self.changed_files)

        return Stats(additions=additions, deletions=deletions)


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

    @property
    def label(self) -> str | None:
        """
        Returns a human-readable label describing the type of this file.
        """
        match self.path.suffix:
            case ".md":
                return "Markdown"
            case ".py":
                return "Python"
            case ".pyi":
                return "Python type stub"
            case ".toml":
                return "TOML"
            case ".yml":
                return "YAML"

        if self.path.name.endswith("requirements.txt"):
            return "pip requirements file"

        if self.path.name.endswith("requirements.in"):
            return "pip-compile input file"

        return None

    @property
    def lang(self) -> str:
        """
        Returns a Pygments lexer shortname for this file.
        """
        match self.path.suffix:
            case ".md":
                return "markdown"
            case ".py" | ".pyi":
                return "python"
            case ".toml":
                return "toml"
            case ".yml":
                return "yaml"
        return "text"


def list_files_for_tree(tree: pygit2.Tree, parent: Path = Path("")) -> list[GitFile]:
    """
    Read a list of files for a tree.
    """
    result: list[GitFile] = []

    for obj in tree:
        name = obj.name
        assert isinstance(name, str), name
        path = parent / name

        if isinstance(obj, pygit2.Blob):
            result.append(
                GitFile(
                    path=path,
                    blob_id=as_hex(obj.id),
                    size=obj.size,
                    is_binary=obj.is_binary,
                )
            )
        elif isinstance(obj, pygit2.Tree):
            result.extend(list_files_for_tree(obj, parent=path))
        else:  # pragma: no cover
            raise TypeError(f"found non-blob/tree in tree: {obj!r}")

    return result


class NavigableFile(BaseModel):
    """
    NavigableFile is a single file in a navigable tree.
    """

    name: str
    is_binary: bool = False


class NavigableTree(BaseModel):
    """
    NavigableTree is enough information to construct the browsable view
    of the entire tree in /files/.
    """

    folders: OrderedDict[Path, "NavigableTree"] = OrderedDict()
    files: list[NavigableFile] = []

    @classmethod
    def from_files(cls, files: Iterable[GitFile]) -> "NavigableTree":
        """
        Construct a NavigableTree from a list of paths.
        """
        root = NavigableTree()

        for f in sorted(files, key=lambda f: f.path):
            p = f.path
            current = root

            # Iterate through the parts of the folder path, and drill
            # down into the correct level of the NavigableTree.
            for part in p.parent.parts:
                part_path = Path(part)
                if part_path not in current.folders:
                    current.folders[part_path] = NavigableTree()
                current = current.folders[part_path]

            current.files.append(NavigableFile(name=p.name, is_binary=f.is_binary))

        root._compress()
        return root

    def _compress(self) -> None:
        """
        Recursively collapse folder segments that only contain a single
        subfolder and no files.
        """
        for path_part, child_tree in list(self.folders.items()):
            # Recursively compress the child first, so we go bottom-up
            # through the tree.
            child_tree._compress()

            # If the child tree only has a single folder, collapse the
            # path parts together.
            if len(child_tree.folders) == 1 and not child_tree.files:
                sub_path, sub_node = child_tree.folders.popitem()
                del self.folders[path_part]
                self.folders[path_part / sub_path] = sub_node

        self.folders = OrderedDict(sorted(self.folders.items()))


class GitTree(BaseModel):
    """
    GitTree describes all the files in the HEAD of the repo.
    """

    files: list[GitFile]

    @classmethod
    def from_repo(cls, repo: pygit2.Repository) -> Self:
        """
        Construct an instance of `GitTree` for the HEAD of a repository.
        """
        commit = repo.get(repo.head.target)
        assert isinstance(commit, pygit2.Commit)

        files = list_files_for_tree(commit.tree)

        return GitTree(files=files)

    @property
    def navigable_tree(self) -> NavigableTree:
        """
        Construct a navigable tree for the /files/ page.
        """
        return NavigableTree.from_files(self.files)


class GitRepository(BaseModel):
    """
    A GitRepository is a repository I wrote that I want to publish
    on /projects/.

    This class reads most of the repo information in the __init__ method,
    so I can do fast lookups later. This is fast enough for small repos;
    I'll likely need to add caching for bigger repos.
    """

    name: str
    description: str
    repo_root: Path

    # The HEAD of the repo, as a hex commit ID.
    head: str

    # All the commits in the repository
    commits: OrderedDict[str, Commit]

    # All the tags in the repository, ordered in descending numerical order
    # TODO(2026-04-16): Read tag annotations to make this more useful
    tags: OrderedDict[str, str]

    # A working directory for the HEAD of the repository
    tree: GitTree

    def __init__(self, name: str, description: str, repo_root: Path):
        """
        Read all the repo information.
        """
        repo = pygit2.Repository(repo_root)

        assert isinstance(repo.head.target, pygit2.Oid), repo.head.target
        head = as_hex(repo.head.target)

        commits = OrderedDict(
            [
                Commit.from_pygit2_commit(repo, commit)
                for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL)
            ]
        )

        tags = OrderedDict()
        for t in repo.references.iterator(ReferenceFilter.TAGS):
            assert isinstance(t.raw_target, pygit2.Oid)
            tags[t.shorthand] = as_hex(t.raw_target)
        tags = sort_tags(tags)

        tree = GitTree.from_repo(repo)

        super().__init__(
            name=name,
            description=description,
            repo_root=repo_root,
            head=head,
            commits=commits,
            tags=tags,
            tree=tree,
        )

    @property
    def navigable_tree(self) -> NavigableTree:
        """
        Return a navigable tree for the /files/ page.
        """
        return self.tree.navigable_tree

    @property
    def last_updated(self) -> datetime:
        """
        Return the date of the most recent update to the repo.
        """
        for commit in self.commits.values():
            return commit.date

        raise TypeError(
            "cannot get last_updated for an empty repo!"
        )  # pragma: no cover

    def readme_contents(self) -> str:
        """
        Return the contents of the README.md file in the root of the repo.
        """
        repo = pygit2.Repository(self.repo_root)

        head = repo.get(repo.head.target)
        assert isinstance(head, pygit2.Commit)

        readme = head.tree / "README.md"
        assert isinstance(readme, pygit2.Blob)

        return readme.data.decode("utf8")

    def get_blob_data(self, blob_id: str) -> bytes:
        """
        Return the contents of a given blob.
        """
        repo = pygit2.Repository(self.repo_root)

        blob = repo.get(blob_id)
        assert isinstance(blob, pygit2.Blob), blob
        return blob.data

    def write_archive(self, out_dir: Path) -> Path:
        """
        Write a tar.gz file with the current HEAD of the repo.

        Returns the path to the created archive.
        """
        repo = pygit2.Repository(self.repo_root)

        head = repo.head
        assert isinstance(head.target, pygit2.Oid)
        archive_id = as_hex(head.target)

        out_path = out_dir / f"{self.name}-{archive_id}.tar.gz"

        # If there's already a file with this name, assume it's correct
        # and continue.
        if out_path.exists():
            return out_path

        # Write to a temporary file first and rename it into place,
        # so writes are atomic.
        tmp_path = out_dir / f"{self.name}-{archive_id}.{uuid.uuid4()}.tar.gz"
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(tmp_path, "w") as out_file:
            repo.write_archive(head.target, out_file)
        tmp_path.move(out_path)

        # Look for other files with the same prefix and clean them up,
        # so I only have the latest download.
        for f in out_dir.iterdir():
            if f.name.startswith(f"{self.name}-") and f != out_path:
                f.unlink()

        return out_path

    def create_clone_for_serving(self, out_dir: Path) -> None:
        """
        Write a bare Git repo with the contents of this repo that can
        be served over HTTPS.

        Any existing clone in this folder will be replaced.
        """
        assert out_dir.name == f"{self.name}.git"

        # Garbage collect the existing repo, which will clear up orphaned
        # objects and create packfiles which can be served more efficiently
        # than tiny per-object files.
        subprocess.check_call(
            ["git", "gc", "--aggressive"], cwd=self.repo_root, stderr=subprocess.DEVNULL
        )

        # Clear the existing folder
        try:
            shutil.rmtree(out_dir)
        except FileNotFoundError:
            pass

        # Create a bare clone of the repository into this folder.
        pygit2.clone_repository(url=self.repo_root, path=out_dir, bare=True)

        # Use git-update-server-info to create a packs and refs file
        # with extra information to help "dumb servers".
        subprocess.check_call(["git", "update-server-info"], cwd=out_dir)

        # Clear out some files which are part of a Git clone but
        # aren't necessary for serving.
        (out_dir / "description").unlink()
        (out_dir / "FETCH_HEAD").unlink()

        shutil.rmtree(out_dir / "hooks")

        # Write a minimal `config` file to remove any personal settings
        # and other data I don't want to share in the clone.
        (out_dir / "config").write_text(
            "[core]\n"
            "	bare = true\n"
            "	repositoryformatversion = 0\n"
            "	filemode = true\n"
        )


def sort_tags(tags: OrderedDict[str, str]) -> OrderedDict[str, str]:
    """
    Sort the tags into human-readable numeric order.
    """
    if all(re.match(r"^v[0-9]+$", t) for t in tags):
        return OrderedDict(
            sorted(
                tags.items(), key=lambda tc: int(tc[0].replace("v", "")), reverse=True
            )
        )
    else:
        return tags


class Project(BaseModel):
    """
    Defines a project to be published in my /projects/ page.
    """

    name: str
    description: str
    git_dir: Path
