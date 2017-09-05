# alexwlchan.net

This repo contains the source code for <https://alexwlchan.net>.

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
