# -*- encoding: utf-8

import feedvalidator
from feedvalidator import compatibility
from feedvalidator.formatter.text_plain import Formatter


def test_feed_passes_validation():
    events = feedvalidator.validateStream(
        open('_site/feeds/all.atom.xml'),
        firstOccurrenceOnly=1
    )['loggedEvents']

    events = compatibility.AA(events)
    output = Formatter(events)
    assert not output, '\n'.join(output)
