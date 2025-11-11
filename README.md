# alexwlchan.net

[![build_site](https://github.com/alexwlchan/alexwlchan.net/actions/workflows/build_site.yml/badge.svg)](https://github.com/alexwlchan/alexwlchan.net/actions/workflows/build_site.yml)

This repo has the code for my personal site, [alexwlchan.net][root], which is a static site built with [Jekyll][jekyll].
It includes a number of plugins I've written to customise the site.

<img src="screenshot_2021-08-30_2x.png" srcset="screenshot_2021-08-30_1x.png 1x, screenshot_2021-08-30_2x.png 2x" alt="Screenshot of the front page of my website">

[root]: https://alexwlchan.net
[jekyll]: https://jekyllrb.com/



## Key tools

The site uses:

*   [Jekyll][jekyll], which generates the HTML pages
*   [Sass][sass], for building the CSS and stylesheets
*   [GitHub Actions][github_actions], which builds and deploys the site
*   [Caddy], which is the web server

When I want to make a change, I open a pull request.
This triggers a build with GitHub Actions, and as part of the build it checks the HTML with [HTMLProofer].
This checks for missing alt text, broken links, invalid HTML, and so on.

If the site passes checks, it's [automatically merged][automerge], and the build on the `main` branch publishes the change to my web server.

[jekyll]: https://jekyllrb.com/
[sass]: https://sass-lang.com/
[github_actions]: https://github.com/features/actions
[Caddy]: https://caddyserver.com/
[HTMLProofer]: https://github.com/gjtorikian/html-proofer
[automerge]: https://github.com/alexwlchan/auto_merge_my_pull_requests



## Building the site

You need Git, Ruby, and Python installed.

To run a local copy of the site:

```console
$ git clone git@github.com:alexwlchan/alexwlchan.net.git

$ python3 -m venv .venv
$ pip install -r requirements.txt

$ bundle install

$ bundle exec jekyll serve
```

The site should be running on <http://localhost:5757>.
If you make changes to the source files, it will automatically update.

To build a one-off set of static HTML files:

```console
$ bundle exec jekyll build
```

This creates a set of HTML files in `_site`.



## How the site works

I publish the source code so other people can see how the site works, and maybe use some of the ideas for their own sites.
This is a list of things that I think are interesting or unusual:

*   [Atom feed generation](docs/atom-feed-generation.md)
*   [No-JavaScript Twitter embeds](docs/twitter-embeds.md)
*   [Linking to my work on other sites](docs/linking-to-other-work.md)
*   [Validating the front matter in Markdown files](docs/front_matter.md)



## Contributing

This is my personal website, so I'm not looking for feature requests or major contributions.

I'd love to get bug reports, especially about accessibility issues, browser rendering inconsistencies, and general usability feedback.
I'm also happy to receive pull requests with typo fixes.

If you want to use any of the components in your own projects – plugins, layouts, stylesheets – feel free to do so.



## License

-   Except where otherwise noted, the site and the associated code are dual-licensed as:

    -   [Creative Commons Attribution 4.0 International (aka CC&nbsp;BY&nbsp;4.0)](https://creativecommons.org/licenses/by/4.0/)
    -   [The MIT License](https://opensource.org/licenses/MIT)

    If you're reusing my content, you can use whichever licence is most appropriate.

    Mostly the CC&nbsp;BY is fine, but Creative Commons licenses [aren't suitable for code][cc_code], so I have MIT as an alternative.

-   Some images that are being used under Creative Commons licenses from other people; see the post where an image is used for attribution.

-   All the icons on the site are used under a royalty-free license from [The Noun Project]; there should be comments in the SVG files indicating their source.
    The original icon authors retain copyright.

[cc_code]: https://wiki.creativecommons.org/index.php/Frequently_Asked_Questions#Can_I_apply_a_Creative_Commons_license_to_software.3F
[The Noun Project]: https://thenounproject.com/pricing/
