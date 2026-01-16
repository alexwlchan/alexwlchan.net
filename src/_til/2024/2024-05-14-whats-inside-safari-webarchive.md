---
layout: til
date: 2024-05-14 18:41:25 +01:00
title: What's inside a Safari webarchive?
summary: |
  The inside of a `.webarchive` file is a binary property list with the complete responses and some request metadata.
tags:
  - safari
  - digital preservation
---
I've been doing a bit of poking around in the Safari [webarchive file format][wiki], and one of the things I wanted to check is that the data isn't stored in some sort of proprietary, impossible-to-read format.
I haven't written a complete piece of code to get the data out, but I've done enough to satisfy myself that if Safari somehow disappears, I could still read it.

I made these notes on Safari 17.4 in macOS Sonoma.

Some notes:

*   **What exactly is it?**
    I thought it might be a zip archive (which is often how Apple bundles up discrete files), but changing the extension to `.zip` and trying to extract it fails.
    
    Are there any clues in the first few bytes?
    Yes!
    
    ```console
    $ head -c 10 example.webarchive
    bplist00�⏎
    ```
    
    So it's a binary [property list] file.
    This fact is also mentioned in the Wikipedia article, but I hadn't read that yet.

*   **Here's the structure of the plist.**
    I got this by changing the file extension to `.plist` and opening it with TextMate, which can pretty-print property lists.

    ```
    // !!! BINARY PROPERTY LIST WARNING !!!
    //
    // The pretty-printed property list below has been created
    // from a binary version on disk and should not be saved as
    // the ASCII format is a subset of the binary representation!
    //
    { WebMainResource = {
        WebResourceData = <3C21444F 43545950 …>;
        WebResourceFrameName = "";
        WebResourceMIMEType = "text/html";
        WebResourceTextEncodingName = "UTF-8";
        WebResourceURL = "https://alexwlchan.net/";
      };
      WebSubresources = (
        { WebResourceData = <EFBBBF3A 726F6F74 …>;
          WebResourceMIMEType = "text/css";
          WebResourceResponse = <62706C69 73743030 …>;
          WebResourceTextEncodingName = "utf-8";
          WebResourceURL = "https://alexwlchan.net/static/style.css?md5=ae9f4dffb52e1062d7fec29497a1eb50";
        },
        { WebResourceData = <89504E47 0D0A1A0A …>;
          WebResourceMIMEType = "image/png";
          WebResourceResponse = <62706C69 73743030 …>;
          WebResourceURL = "https://alexwlchan.net/theme/white-waves-transparent.png";
        },
        { WebResourceData = <00000020 66747970 …>;
          WebResourceMIMEType = "image/avif";
          WebResourceResponse = <62706C69 73743030 …>;
          WebResourceURL = "https://alexwlchan.net/images/profile_green_square_1x.avif";
        },
      );
    }
    ```
    
    The two binary fields are:
    
    *   `WebResourceData`, which contains the raw bytes of the response.
        As best I can tell, this is unmodified and doesn't, for example, update references to other resources in the webarchive.

    *   `WebResourceResponse`, which is another binary plist with a bunch of response metadata, including HTTP response headers.
        Notably, in my example these include the [Date header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Date), so I can tell when the archive was generated.
        
    It would be a bit of work to turn this into a usable collection of files -- I could export them into standalone files fairly easily, but then I'd have to work out how to make all the references work, e.g. making sure the HTML file looks in the right place for the CSS file.

*   **I can open it using [plistlib] in the Python standard library.**
    I don't have to rely on Safari!
    
    ```python
    import plistlib

    with open("example.webarchive", "rb") as infile:
        archive = plistlib.load(infile)
    ```

    This returns a large dict, which is helpful for exploring and seeing the raw binary data.
    I suspect there are better tools for opening property lists, because the `WebResourceResponse` plist in particular seems quite awkward using this library -- but even if Python was all I had available, it's enough to do something useful. 

[wiki]: https://en.wikipedia.org/wiki/Webarchive
[property list]: https://en.wikipedia.org/wiki/Property_list
[plistlib]: https://docs.python.org/3/library/plistlib.html
