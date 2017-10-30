# -*- encoding: utf-8

import os

import attr
import frontmatter
import pytest

_front_matters = []


@attr.s
class SourceFile(object):
    path = attr.ib()
    metadata = attr.ib()


@pytest.fixture
def front_matters(src):
    """
    Use os.walk() to inspect every source file, and return a list of metadata
    blobs and the associated file.
    """
    if not _front_matters:
        for root, _, filenames in os.walk(src):
            for entry in filenames:
                if not entry.endswith('.md'):
                    continue

                path = os.path.join(root, entry)
                display_path = path.replace('/repo/', '')
                metadata = frontmatter.load(path).metadata
                src_f = SourceFile(path=display_path, metadata=metadata)
                _front_matters.append(src_f)

    return _front_matters


def test_every_front_matter_has_layout(front_matters):
    missing_layout = [f for f in front_matters if 'layout' not in f.metadata]
    bad_paths = [f.path for f in missing_layout]
    print('\n'.join(bad_paths))
    assert len(bad_paths) == 0
