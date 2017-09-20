# -*- encoding: utf-8

import pytest

feedvalidator = pytest.importorskip('feedvalidator')

from feedvalidator import compatibility
from feedvalidator.formatter.text_plain import Formatter


def test_feed_is_valid_atom():
    try:
        events = feedvalidator.validateURL(
            'http://0.0.0.0:5757/feeds/all.atom.xml', firstOccurrenceOnly=1
        )['loggedEvents']
    except feedvalidator.logging.ValidationFailure as vf:
        events = [vf.event]

    events = compatibility.AA(events)
    output = Formatter(events)
    print('\n'.join(output))
    assert len(events) == 0
