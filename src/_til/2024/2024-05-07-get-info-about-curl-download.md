---
layout: til
date: 2024-05-07 20:54:36 +01:00
title: How to get the filename/size without downloading a file in curl
summary: |
  You can do some fun stuff with the `--write-out` flag and variables.
tags:
  - curl
---
I was doing some stuff with curl, and I found some uses for the `--write-out` flag (which Daniel Stenberg has described as [“one of \[his\] personal favorites”](https://daniel.haxx.se/blog/2023/08/01/curl-write-out-to-files/)).

I was using curl to download snapshots from Wikimedia Commons, and I wanted to know:

* If I use [the `--remote-name` flag](https://curl.se/docs/manpage.html#-O) and let curl use the name based on the remote file, what filename will it save to?
* How big is the downloaded file going to be?

curl clearly knows both of these things because it uses them as part of the download process, but I wanted to get them separately so I could write some wrapper scripts around them.

*   To get the filename that curl will write a file to, use `--write-out` with the `filename_effective` variable:

    ```console
    $ curl --head --remote-name --write-out '%{filename_effective}' "$url"
    ```

*   To get the final size of the file that will be downloaded, use `--write-out` and log the [value of the Content-Length header](https://everything.curl.dev/usingcurl/verbose/writeout.html#http-headers):

    ```console
    $ curl --head --write-out '%header{content-length}' "$url"
    ```

Obviously both of these rely on having a relatively well-behaved web server that doesn't change filenames and returns a true value in the `Content-Length` header -- which is sufficient for a lot of simple scripting and dealing with trusted downloads.

---

By default, the `--head` flag will print a complete list of headers.
If you want to suppress this and just print the value of `--write-out`, you need to add `--silent` and `--output /dev/null`, for example:

```console
$ curl --head --silent --output /dev/null --write-out '%header{content-length}' "$url"
```
