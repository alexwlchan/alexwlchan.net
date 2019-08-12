---
layout: post
title: Removing the DRM from my Kindle books
summary: Links to a couple of projects that I found helpful when trying to strip the DRM from my Kindle books.
category: Programming and code
---

A few months ago, Microsoft made headlines when they announced they'd be [turning off people's ebooks][microsoft].
They were turning off the DRM servers behind their store, and refunding customers for any books they'd bought.
I never bought anything on the Microsoft ebook store, but I do have a collection of Kindle books, and this story was a reminder to investigate ways to strip the DRM from those.

Google suggests that [Calibre][calibre] can do this with the right plugins, but I don't use Calibre for anything else.
I prefer solutions that use command-line tools and (ideally) run inside Docker container – they tend to be much more portable between machines.

I've got a script that works now, which leans on two other bits of software to do the heavy lifting:

*   **Stripping the DRM: [ch33s3w0rm/kindle_dedrm](https://github.com/ch33s3w0rm/kindle_dedrm).**
    This is a Python script which strips the DRM from an encrypted Kindle book.
    The encryption in a given file is tied to your device, so you'll need your Kindle's serial number to perform the decryption.

    It runs in Python 2, no dependencies required:

    ```console
    $ git clone https://github.com/ch33s3w0rm/kindle_dedrm.git
    $ cd kindle_dedrm
    $ python2 kindle_dedrm.py --kindle=<KINDLE_SN> /path/to/encrypted_book.azw
    ```

    It creates a DRM-free AZW file alongside the original file.

*   **Converting AZW to EPUB: [ebook-convert].**

    The AZW format is Kindle-specific; if I read my books on anything else, I need to create a copy as an EPUB.

    There are online converters that take an AZW and return an EPUB, but I feel uncomfortable doing file conversion via a third-party service.

    You can do this with the Calibre GUI app, or its bundled command-line tool, [ebook-convert].
    The latter lets you convert ebooks between formats in a script, and that's what I really want.
    I found a [Docker image that includes Calibre][docker], and I override the entrypoint to invoke the command-line tool:

    ```console
    $ docker run --rm \
        --volume $(pwd):$(pwd) \
        --entrypoint ebook-convert \
        $(pwd)/unencrypted_book.azw unencrypted_book.epub
    ```

    And now I have two copies of my book: an AZW to use on my Kindle, and an EPUB to use everywhere else.

My script has a couple of extra pieces to upload the files to my ebook manager, which are very specific to my setup -- the software I've linked above is more general, and hopefully useful links for anybody else who wants to strip the DRM from their Kindle books.

[microsoft]: https://www.theverge.com/2019/4/2/18292177/microsoft-ebooks-refund-stops-selling-digital-books-store
[calibre]: https://calibre-ebook.com/
[ebook-convert]: http://manpages.ubuntu.com/manpages/bionic/man1/ebook-convert.1.html
[docker]: https://hub.docker.com/r/regueiro/calibre-server
