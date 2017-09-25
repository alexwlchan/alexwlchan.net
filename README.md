# alexwlchan.net

[![Build Status](https://travis-ci.org/alexwlchan/alexwlchan.net.svg?branch=master)](https://travis-ci.org/alexwlchan/alexwlchan.net)

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

### Builds in Docker

I used Jekyll (well, [Octopress][octopress]) for the first iteration of my site, but I kept having issues with Ruby.
Half the time, I'd come to write something, and find I was unable to build the site!
Clearly sub-optimal.

Drawing inspiration [from what we do at Wellcome][platform], I've pushed the entire build process inside Docker.
When I want to build the site on a new machine, I don't need to worry about installing dependencies – it's managed entirely by Docker.

[octopress]: http://octopress.org/
[platform]: https://github.com/wellcometrust/platform

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

The theme colour is also used in the favicon (which has to be created manually) and in the header image (which is created automatically using [specktre][specktre]).

The heavy lifting is done in [`_plugins/theming.rb`](src/_plugins/theming.rb).

[specktre]: https://pypi.org/project/specktre/
[docopt_green]: https://alexwlchan.net/2017/09/ode-to-docopt/

### Other theming settings

In the same vein as page colour, I can override a couple of other settings in the `theme:` front matter.
Specifically:

```yaml
theme:
  card_type: summary_large_image    # If I want to change the Twitter card type
                                    # https://dev.twitter.com/cards/overview
  image: /images/2017/P5280917_2x.jpg
                                    # If I'm using summary_large_image, a path
                                    # to the image to use
  touch_icon: docopt                # Override the apple-touch-icon setting,
                                    # and the icon used in social sharing links
```

These settings are used in the template logic.
The assets get saved in the [`theme`](src/theme) directory, and have to be created manually.

### Static file copying

I have a plugin [`static_file_generator.rb`](src/_plugins/static_file_generator.rb) which copies static files (images, videos, slides) into the output directory using rsync.

This is to speed up site generation times – it's an idea I got from [Wolf Rentzsch][rentzsch].

[rentzsch]: http://rentzsch.tumblr.com/post/58936832594/speed-up-jekyll-using-one-weird-trick

### Month and year archives

The format of my post URLs is:

```
/:year/:month/:title/
```

Because I'm old-fashioned and think URLs are meaningful, it feels to me that `/:year/:month/` should show you a collection of all the posts in that month, and `/:year/` should do the same for the year.
The path can be treated as a directory structure – which it is, if you look at the generated files!

To that end, I'm using [another plugin](src/_plugins/archive_generator.rb) to generate them just the way I like.
It's a fork of [jekyll-monthly-archive-plugin][archive], but with my own template and support for yearly archives as well.

[archive]: https://github.com/shigeya/jekyll-monthly-archive-plugin

### Twitter embeds

For embedded tweets, rather than using Twitter's embed function (which comes with all sorts of JavaScript and tracking and slowness), I render tweets as static HTML.
This is an idea I originally got [from Dr. Drang][drangtweet].

To embed a tweet in a post, I use the following tag:

```plain
{% tweet https://twitter.com/iamkimiam/status/848188958567800832 %}
```

When the site is built, I have [a personal plugin](src/_plugins/twitter.rb) that:

*   Polls the Twitter API
*   Caches the complete API response and a copy of the author's avatar
*   Uses the cached API response and a template to render an HTML snippet

Polling the Twitter API requires a set of API tokens, but I check in the cached responses (see `_tweets`).
This means that I can fetch the tweet data on a local machine, but when I push to Travis, it doesn't need my credentials to render the tweet.

Because I render the tweets at compile time, I can change the appearance of old tweets by updating the template, without having to edit old posts.
That's part of why I keep the entire API response – in case I later need data I'd thrown away the first time.

[drangtweet]: http://www.leancrew.com/all-this/2012/07/good-embedded-tweets/

## Contributing

I'm only interested in hearing about bugs or typos – please don't open an issue because you think I'm a terrible writer! 😜

If you want to use any of the components – plugins, layouts, stylesheets – feel free to do so.
Everything is MIT licensed, unless otherwise noted.
