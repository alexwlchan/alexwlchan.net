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

The site is built with Jekyll running inside a Docker container.
You need Git, Make and Docker installed.

Clone the repository from GitHub:

```console
$ git clone git@github.com:alexwlchan/alexwlchan.net.git
```

To build the HTML pages for the site:

```console
$ make build
```

For continuous testing, run:

```console
$ make serve
```

A local copy of the site will be served on <http://localhost:5757>.
If you make changes to the source files, this version will automatically update.
