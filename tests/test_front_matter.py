# -*- encoding: utf-8

import datetime as dt
import os

import attr
import dateutil.parser as dp
import frontmatter
import pytest

_front_matters = []


@attr.s
class SourceFile(object):
    path = attr.ib()
    metadata = attr.ib()

    @property
    def date(self):
        if '_drafts' in self.path:
            return dt.datetime.now().date()
        try:
            return dp.parse(self.metadata['date']).date()
        except KeyError:
            if self.metadata['layout'] == 'post':
                parts = os.path.basename(self.path).split('-')
                return dt.date(
                    year=int(parts[0]),
                    month=int(parts[1]),
                    day=int(parts[2])
                )
            elif self.metadata['layout'] in ('blog', 'home', 'page', 'talks'):
                return dt.datetime.now().date()
            else:
                raise RuntimeError(
                    "Unrecognised layout: %s" % self.metadata['layout']
                )

    @property
    def tags(self):
        try:
            return [t.strip() for t in self.metadata['tags'].split()]
        except KeyError:
            return []


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


@pytest.fixture
def new_front_matters(front_matters):
    """
    Front matters that were created after a certain date -- older posts are
    not (yet) subject to these tests.
    """
    return [f for f in _front_matters if f.date >= dt.date(2017, 10, 1)]


def test_every_post_has_summary(new_front_matters):
    missing_summary = [
        f for f in new_front_matters
        if (f.metadata['layout'] == 'post') and (
            ('summary' not in f.metadata) or
            (f.metadata['summary'] is None)
        )
    ]
    bad_paths = [f.path for f in missing_summary]
    print('\n'.join(bad_paths))
    assert len(bad_paths) == 0


def test_tags_dont_contain_slashes(front_matters):
    has_tags = [f for f in front_matters if f.tags]
    bad_tags = [f for f in front_matters if any('/' in t for t in f.tags)]
    bad_paths = ['%s (%s)' % (f.path, f.tags) for f in bad_tags]
    print('\n'.join(bad_paths))
    assert len(bad_paths) == 0
