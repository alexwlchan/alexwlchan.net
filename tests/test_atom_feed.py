# -*- encoding: utf-8

import feedvalidator
from feedvalidator import compatibility
from feedvalidator.formatter.text_plain import Formatter
import pytest


def test_feed_is_valid_atom(hostname):
    atom_url = 'http://%s/feeds/all.atom.xml' % hostname
    try:
        events = feedvalidator.validateURL(
            atom_url, firstOccurrenceOnly=1
        )['loggedEvents']
    except feedvalidator.logging.ValidationFailure as vf:
        events = [vf.event]

    events = compatibility.AA(events)
    output = Formatter(events)
    print('\n'.join(output))
    assert len(events) == 0
