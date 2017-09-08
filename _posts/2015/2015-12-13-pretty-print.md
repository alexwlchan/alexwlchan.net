---
date: 2015-12-13 17:15:00 +0000
layout: post
slug: pretty-print
tags: shell scripting
title: Pretty printing JSON and XML in the shell
---

Last year I read Craig Hockenberry's [magnus opus](http://furbo.org/2014/09/03/the-terminal/) – a huge collection of information about the OS X Terminal and the Bash shell.
It's worth reading in its entirety, even if you don't use a Mac.
My favourite tips were opt-clicking to jump around in Terminal (which makes Vim far more usable for me), and using the `lsof` command when a disk won't eject.
Both super useful.

At the same time, I read [Dr. Drang's suggestion](http://www.leancrew.com/all-this/2014/09/chock-amok/) that we write up our own tips.
I wrote this post at the time, and then it sat in drafts for over a year.
Oops.
Anyway, here are a few tips from me.

I work a lot with website APIs, which typically return responses that are formatted in XML or JSON.
To save bandwidth, these responses are [minified](https://en.wikipedia.org/wiki/Minification_(programming)) (stripped of unnecessary whitespace and newlines).
That's fine for a program, but it's quite painful if I'm reading it.

Luckily, OS X includes a few tools for pretty printing JSON and XML.
This makes the responses substantially easier to read for a human.

<!-- summary -->

<!--

    ```console
$ curl "https://api.tumblr.com/v2/blog/staff.tumblr.com/avatar"
{"meta":{"status":301,"msg":"Found"},"response":{"avatar_url":"https:\/\/38.media.tumblr.com\/avatar_0d81f376bcbd_64.png"}}

$ curl "https://api.tumblr.com/v2/blog/staff.tumblr.com/avatar" | python -m json.tool
{
    "meta": {
        "msg": "Found",
        "status": 301
    },
    "response": {
        "avatar_url": "https://38.media.tumblr.com/avatar_0d81f376bcbd_64.png"
    }
}
```

-->

*   To tidy up JSON, pipe the output to `python -m json.tool`:

    <div class="codehilite"><pre><span></span><span class="gp">$</span> curl <span class="s2">"https://api.tumblr.com/v2/blog/staff.tumblr.com/avatar"</span>
    <span class="go">{"meta":{"status":301,"msg":"Found"},"response":{"avatar_url":"https:\/\/38.media.tumblr.com\/avatar_0d81f376bcbd_64.png"}}</span>

    <span class="gp">$</span> curl <span class="s2">"https://api.tumblr.com/v2/blog/staff.tumblr.com/avatar"</span> <span class="p">|</span> python -m json.tool
    <span class="go">{</span>
    <span class="go">    "meta": {</span>
    <span class="go">        "msg": "Found",</span>
    <span class="go">        "status": 301</span>
    <span class="go">    },</span>
    <span class="go">    "response": {</span>
    <span class="go">        "avatar_url": "https://38.media.tumblr.com/avatar_0d81f376bcbd_64.png"</span>
    <span class="go">    }</span>
    <span class="go">}</span></pre></div>

    When you invoke Python with the `-m` flag, it executes a [module as a script](https://www.python.org/dev/peps/pep-0338/) – as if you ran the file directly.
    The [json.tool](https://docs.python.org/3.5/library/json.html?highlight=json.tool#module-json.tool) module acts as a pretty printer for text received on stdin.
    It also has extra arguments for writing the output to a file, or sorting the keys.

    Since the json module is part of Python's standard library, this will work on any system that has Python installed.

<!--
    There's a bit of a cheat here: the lnk attribute is actually link,
    but if you use that then lxml/mincss try to read it as a CSS attribute
    and fall over.
-->

<!-- ```console
$ curl "http://xkcd.com/rss.xml"
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>xkcd.com</title><lnk>http://xkcd.com/</lnk><description>xkcd.com: A webcomic of romance and math humor.</description><language>en</language><item><title>Red Car</title> ...

$ curl "http://xkcd.com/rss.xml" | xmllint --format -
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>xkcd.com</title>
    <lnk>http://xkcd.com/</lnk>
    <description>xkcd.com: A webcomic of romance and math humor.</description>
    <language>en</language>
    <item>
      <title>Red Car</title>
...
``` -->

*   To tidy up XML, pipe the output to `xmlint --format -`:

    <div class="codehilite"><pre><span></span><span class="gp">$</span> curl <span class="s2">"http://xkcd.com/rss.xml"</span>
    <span class="go">&lt;?xml version="1.0" encoding="utf-8"?&gt;</span>
    <span class="go">&lt;rss version="2.0"&gt;&lt;channel&gt;&lt;title&gt;xkcd.com&lt;/title&gt;&lt;link&gt;http://xkcd.com/&lt;/lnk&gt;&lt;description&gt;xkcd.com: A webcomic of romance and math humor.&lt;/lnk&gt;&lt;/description&gt;&lt;language&gt;en&lt;/language&gt;&lt;item&gt;&lt;title&gt;Red Car&lt;/title&gt; ...</span>

    <span class="gp">$</span> curl <span class="s2">"http://xkcd.com/rss.xml"</span> <span class="p">|</span> xmllint --format -
    <span class="go">&lt;?xml version="1.0" encoding="utf-8"?&gt;</span>
    <span class="go">&lt;rss version="2.0"&gt;</span>
    <span class="go">  &lt;channel&gt;</span>
    <span class="go">    &lt;title&gt;xkcd.com&lt;/title&gt;</span>
    <span class="go">    &lt;link&gt;http://xkcd.com/&lt;/link&gt;</span>
    <span class="go">    &lt;description&gt;xkcd.com: A webcomic of romance and math humor.&lt;/description&gt;</span>
    <span class="go">    &lt;language&gt;en&lt;/language&gt;</span>
    <span class="go">    &lt;item&gt;</span>
    <span class="go">      &lt;title&gt;Red Car&lt;/title&gt;</span>
    <span class="go">...</span></pre></div>

    This is just the tip of what xmllint can do – and it turns out Apple has been quietly including it since [at least Mavericks](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/xmllint.1.html).
    It's available in the package manager of most Linux distros.

    I don't use the advanced features much – once I want to start unpicking the XML, I break out Python and the [xml.etree module](https://docs.python.org/3.5/library/xml.etree.elementtree.html?highlight=elementtree) – but it's useful for quick debugging and raw responses.
