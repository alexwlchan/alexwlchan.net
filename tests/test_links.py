#!/usr/bin/env python
# -*- encoding: utf-8

import pytest
import requests


@pytest.mark.parametrize('path', [
    # Check pagination is working correctly
    '/page/2/', '/page/3/',
])
def test_pages_appear_correctly(hostname, path):
    resp = requests.get('http://%s/%s' % (hostname, path))
    assert resp.status_code == 200


@pytest.mark.parametrize('path, text_in_page', [
    ('2017/', 'Posts from 2017'),
    ('2017/07/', 'Posts from July 2017'),
    ('', 'Older posts'),
    ('', '<title>alexwlchan</title>'),
    ('archive/', '<h3>2017</h3>'),

    # Smartypants is working
    ('2017/09/lazy-reading-in-python', u'kept in Amazon S3 – XML exports'),
    ('2017/09/ode-to-docopt', u'I’ve used it in multiple languages'),

    # Syntax highlighting is being applied correctly
    ('2017/09/useful-git-commands/', '''<code class="language-console" data-lang="console"><span></span><span class="gp">$</span> git rev-parse --show-toplevel
<span class="go">/Users/alexwlchan/repos/alexwlchan.net</span>
</code>'''),

    # We're not adding trailing commas to tags
    ('2017/09/ode-to-docopt', 'python</a>, <a'),

    # I don't really want to minify it twice (and minification might vary
    # in subtle ways), but I can look for blocks which aren't minified in
    # the template and *should* be minified in the output.
    ('feeds/all.atom.xml', '<author><name>Alex Chan</name>'),
    ('feeds/all.atom.xml', '</entry><entry>'),

    # Footnotes are rendered correctly
    ('2017/01/scrape-logged-in-ao3', '<a href="#fn1" rel="footnote">1</a>'),

    # Tweets are being rendered correctly
    ('2014/07/overcast/', '<div class="tweet"><blockquote>'),
    ('2014/07/overcast/', '</blockquote></div>'),
    ('2014/07/overcast/',
     '<a href="https://twitter.com/alexwlchan">@alexwlchan</a>'),
    ('2014/07/overcast', 'so:<br/> Episode 1'),
    ('2017/10/lightning-talks/',
     '<a href="https://twitter.com/hashtag/PyConUK">#PyConUK</a>'),
    ('2017/10/lightning-talks/', '<div class="media">'),
    ('2017/04/lessons-from-alterconf/', '<div class="media">'),
])
def test_text_appears_in_pages(hostname, path, text_in_page):
    resp = requests.get('http://%s/%s' % (hostname, path))
    assert resp.status_code == 200
    assert text_in_page in resp.text


@pytest.mark.parametrize('path, text', [
    # Year markers only appear in the global archives, not year or month pages
    ('2017/', '<h3>2017</h3>'),
    ('2017/07/', '<h3>2017</h3>'),
])
def test_text_does_not_appear_in_pages(hostname, path, text):
    resp = requests.get('http://%s/%s' % (hostname, path))
    assert resp.status_code == 200
    assert text not in resp.text
