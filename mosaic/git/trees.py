"""
Models and functions for interacting with file trees.

This includes abstract file hierarchies and the Git data structure.
"""

from collections import OrderedDict
from collections.abc import Iterable
from pathlib import Path

from pydantic import BaseModel, TypeAdapter
import pygit2

from mosaic.cache import get_cache

from .files import GitFile
from .ids import as_hex


__all__ = ["GitTree", "NavigableFile", "NavigableTree"]


_CACHE = get_cache(".cache/git_trees.db")
_LIST_GIT_FILE_ADAPTER = TypeAdapter(list[GitFile])


def list_files_for_tree_from_git(tree: pygit2.Tree, parent: Path) -> list[GitFile]:
    """
    Read a list of files for a tree directly from Git.
    """
    files: list[GitFile] = []

    for obj in tree:
        name = obj.name
        assert isinstance(name, str), name
        path = parent / name

        if isinstance(obj, pygit2.Blob):
            files.append(
                GitFile(
                    path=path,
                    blob_id=as_hex(obj.id),
                    size=obj.size,
                    is_binary=obj.is_binary,
                )
            )
        elif isinstance(obj, pygit2.Tree):
            files.extend(list_files_for_tree(obj, parent=path))
        else:  # pragma: no cover
            raise TypeError(f"found non-blob/tree in tree: {obj!r}")

    return files


def list_files_for_tree(tree: pygit2.Tree, parent: Path = Path("")) -> list[GitFile]:
    """
    Read a list of files for a tree.

    This result will be cached to avoid repeated work over subsequent
    lookups.
    """
    # Use the Git object SHA as the key, which uniquely identifies trees.
    cache_ns = "list_files_for_tree"
    tree_id = as_hex(tree.id)
    cache_key = f"{tree_id}:{parent}"

    if json_str := _CACHE.get(cache_ns, cache_key):
        return _LIST_GIT_FILE_ADAPTER.validate_json(json_str)
    else:
        files = list_files_for_tree_from_git(tree, parent)
        json_str = _LIST_GIT_FILE_ADAPTER.dump_json(files).decode("utf8")
        _CACHE.set(cache_ns, cache_key, json_str)
        return files


class NavigableFile(BaseModel):
    """
    NavigableFile is a single file in a navigable tree.
    """

    name: str
    is_binary: bool = False


class NavigableTree(BaseModel):
    """
    NavigableTree represents a directory tree structured for navigation
    in a hierarchical UI, with files grouped by directory.
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
    A lookup map of all files in a Git tree snapshot.
    """

    files_by_path: dict[Path, GitFile]

    @property
    def files(self) -> Iterable[GitFile]:
        """
        Return all the files in this repo.
        """
        return self.files_by_path.values()

    def has_file(self, p: Path) -> bool:
        """
        Return True if the repo has a file with this path, False otherwise.
        """
        return p in self.files_by_path

    @classmethod
    def from_repo(cls, repo: pygit2.Repository) -> "GitTree":
        """
        Construct an instance of `GitTree` for the HEAD of a repository.
        """
        commit = repo.get(repo.head.target)
        assert isinstance(commit, pygit2.Commit)

        files = list_files_for_tree(commit.tree)
        tree_data = GitTree(files_by_path={f.path: f for f in files})

        return tree_data

    @property
    def navigable_tree(self) -> NavigableTree:
        """
        Construct a navigable tree for the /files/ page.
        """
        return NavigableTree.from_files(self.files)
