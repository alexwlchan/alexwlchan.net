# alexwlchan.net

This repo has the code for my personal site, [alexwlchan.net][root].
It's a static site built with [Jekyll][jekyll], with a number of plugins written to suit my personal tastes.

The site is built and tested by [Travis][travis].
When I push to master, Travis uploads a copy of the rendered HTML files to a [Linode VPS][linode], where they're served by [nginx][nginx].

![](screenshot.png)

[root]: https://alexwlchan.net
[jekyll]: https://jekyllrb.com/
[travis]: https://travis-ci.org/
[linode]: https://www.linode.com/?r=ba2e6ce21e0c63952a7c74967ea0b96617bd44a3
[nginx]: https://nginx.org/

## Getting started

You need Git, make and Docker installed.

To run a local copy of the site:

```console
$ git clone git@github.com:alexwlchan/alexwlchan.net.git
$ make serve
```

The site should be running on <http://localhost:5757>.
If you make changes to the source files, it will automatically update.

To build a one-off set of static HTML files:

```console
$ make build
```

## Technical details

### Testing in Travis

I run a small number of tests in Travis, which look for particular strings in the rendered HTML.
I'm not trying to test Jekyll itself (that's best left to the Jekyll developers) – more test that I haven't broken something with a config change.
Stuff like footnotes, syntax highlighting, and so on – I have a bad habit of breaking them and not noticing in.

Tests are a good way to document the fiddly details buried in the templates and the like.

### Atom feed generation

For Atom feeds, I have [my own template][atom_template] and a few [custom filters][atom_filter].
I don't use [jekyll-feed][feed] because I sometimes want an entry to link somewhere other than my site (Daring Fireball-style link posts), and that's not supported.

If I want a post to link elsewhere, I add `link` to the post frontmatter:

```yaml
title:  A validator for RSS and Atom feeds
layout: post
date:   2017-09-22 08:19:42 +0100
link:   https://github.com/rubys/feedvalidator
```

Because I'm rolling my own feeds, I use [rubys/feedvalidator][validator] to test I'm really producing valid Atom markup.
See [`tests/test_atom_feed.py`](tests/test_atom_feed.py).

[atom_template]: src/feeds/all.atom.xml
[atom_filter]: src/_plugins/atom_feeds.rb
[feed]: https://github.com/jekyll/jekyll-feed
[validator]: https://github.com/rubys/feedvalidator

### Stylesheets

I write all my stylesheets in SCSS.
The component SCSS files are in [`_scss`](src/_scss), and they're pulled together in `_main.scss`.
The output is a single, minified, CSS file.

The colours and layout variables are defined in `_settings.scss`.
Note that `$primary-color` is defined as follows:

```scss
$primary-color: #d01c11 !default;
```

The `!default` marker means this variable is defined only if it isn't already defined – and I use this to produce alt-colour versions of the stylesheet.
If I add the following front matter to a post:

```yaml
theme:
  color: 6c006c
```

then I get a version of the stylesheet that uses `#6c006c` as its primary colour, and the page loads that stylesheet instead.
You can see an example [in my docopt slides][docopt_green].

The heavy lifting is done in [`_plugins/theming.rb`](src/_plugins/theming.rb).

[docopt_green]: https://alexwlchan.net/2017/09/ode-to-docopt/

### Static file copying

I have a plugin [`static_file_generator.rb`](src/_plugins/static_file_generator.rb) which copies static files (images, videos, slides) into the output directory using rsync.

The idea is to speed up site generation times – it's an idea I got from [Wolf Rentzsch][rentzsch].

[rentzsch]: http://rentzsch.tumblr.com/post/58936832594/speed-up-jekyll-using-one-weird-trick
