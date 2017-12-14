---
layout: post
date: 2014-11-02 16:19:00 +0000
tags: python
title: Unpacking sets and ranges from a single string
---

I was reading the [cURL man page][curl] on Thursday. Although I didn't find what I was looking for, I did come across some rather neat syntax for specifying multiple URLs in a single string. Here's an example:

> You can specify multiple URLs or parts of URLs by writing part sets within braces as in:

> <p class="exampleurl">http://site.**{one,two,three}**.com</p>

> or you can get sequences of alphanumeric series by using [] as in:

> <p class="exampleurl">ftp://ftp.numericals.com/file**[1-100]**.txt<br/>
> ftp://ftp.numericals.com/file**[001-100]**.txt (with leading zeros)<br/>
> ftp://ftp.letters.com/file**[a-z]**.txt</p>

The [man page][curl] has more examples.

I've been thinking about something like this for a while. It's not hard to
create these lists using loops in Python, but it's a bit tedious. It takes time
to set up the correct loops, and for anything complicated you end up with an
unhealthy level of nesting. I'd rather solve this problem once, and then not
have to worry again.

I had a slightly different syntax in mind (simpler, and with more double brackets), but since I had a finished spec in the form of the examples, I decided to use this instead. I've written a Python script which takes a single string, and returns all the strings it specifies as an iterator.

<!-- summary -->

It supports the same syntax as the cURL counterpart. Here's a simple example:

```python
>>> urls = curlparser.parse_string("http://site.{one,two,three}.com")
>>> urls.next()
"http://site.one.com"
>>> urls.next()
"http://site.two.com"
>>> urls.next()
"http://site.three.com"
```

It can also be invoked from the shell:

```console
$ python curlparser.py "ftp://ftp.numericals.com/file[1-5].txt"
ftp://ftp.numericals.com/file1.txt
ftp://ftp.numericals.com/file2.txt
ftp://ftp.numericals.com/file3.txt
ftp://ftp.numericals.com/file4.txt
ftp://ftp.numericals.com/file5.txt
```

I have this bound to a TextExpander snippet, with a fill-in field for the string.

The script itself [is in a Gist][gist], or you can
<a target="_blank" href="/files/curlparser.py">download it directly</a>.
I've also got <a target="_blank" href="/files/curlparser-examples.txt">a list
of examples</a> from the cURL man page.

When I originally thought about this problem, I only had one use-case in mind. It's another project, which has a database with lots of similar strings. I can save on disk space by encoding strings in the database with this compact notation, and only getting the full list when I actually need the strings.

(At the point of adding an entry to the database, I have a compact string, not the full list. Turning the string into the list is easy. The other way looks much harder. Taking an arbitrary list of strings and finding a set of compact strings which specify exactly that list could be an interesting problem, but it's not one I have time to investigate.)

Now that I have the script, I'm seeing lots of new use cases. I'll still be falling back to hand-coding anything particularly complicated, but this seems like a good alternative for anything simple.

[curl]: http://curl.haxx.se/docs/manpage.html
[gist]: https://gist.github.com/alexwlchan/10e1e24ecd354edc5639