# Atom feed generation

For Atom feeds, I have [my own template][atom_template] and a few [custom filters][atom_filter].
I don't use [jekyll-feed][feed] because I sometimes want an entry to link somewhere other than my site (Daring Fireball-style link posts), and that's not supported.

If I want a post to link elsewhere, I add `link` to the post frontmatter:

```yaml
title:  "A validator for RSS and Atom feeds"
layout: "post"
date:   "2017-09-22 08:19:42 +0100"
link:   "https://github.com/rubys/feedvalidator"
```

Because I'm rolling my own feeds, I use [rubys/feedvalidator][validator] to test I'm really producing valid Atom markup.
See [`tests/test_atom_feed.py`](tests/test_atom_feed.py).

[atom_template]: ../src/feeds/all.atom.xml
[atom_filter]: ../src/_plugins/atom_feeds.rb
[feed]: https://github.com/jekyll/jekyll-feed
[validator]: https://github.com/rubys/feedvalidator
