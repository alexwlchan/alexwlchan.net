---
layout: til
title: How to get the target of an HTTP redirect with curl
date: 2024-10-25 07:39:04 +01:00
tags:
  - curl
---
I wanted to check where an HTTP URL redirects using curl.

I came up with the following command:

```shell
# Get the URL where "$url" redirects to (or $url, if it doesn't redirect).
#
# Flags:
#
#   --head             = only fetch the headers, don't download the page
#   --location         = follow redirections
#   --write-out        = print the final URL fetched to stdout
#   --silent           = don't print any progress information
#   --show-error       = show an error message if curl fails
#   --output /dev/null = don't print curl's default output, which would
#                        be the headers from every URL it fetched
#
curl "$url" \
  --head \
  --location \
  --write-out "%{url_effective}" \
  --silent --show-error \
  --output /dev/null
```

If I only want to follow a single redirect, I can add the [`--max-redirs` flag](https://curl.se/docs/manpage.html#--max-redirs).

As I was writing this command, I had a vague memory of the `--write-out` flag -- it's one of Daniel Stenberg's  ["personal favourites"](https://daniel.haxx.se/blog/2023/08/01/curl-write-out-to-files/) and I wrote about using it in [a TIL in May](/til/2024/get-info-about-curl-download/).
