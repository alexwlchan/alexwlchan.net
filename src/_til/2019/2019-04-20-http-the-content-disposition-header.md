---
layout: til
title: "The Content-Disposition header can be used to name a downloaded file"
date: 2019-04-20 21:24:30 +01:00
tags:
  - http
---

The `Content-Disposition` header can be used to tell a browser the filename of an HTTP response.
It's used for "Save As" or when downloading the file.

For example, you might access a URL of the form:

    /files/0645c33f-0be6-44e1-8059-228ec9594867.pdf

If you include a `Content-Disposition` header of the form:

    filename*=utf-8''original_filename.pdf

the browser will download this filename as `original_filename.pdf`.

Read more:

*   MDN docs for Content-Disposition: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition>
*   Encoding a filename as UTF-8: <https://stackoverflow.com/a/49481671/1558022>
