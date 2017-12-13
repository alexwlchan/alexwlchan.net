---
date: 2015-03-07 10:44:00 +0000
layout: post
summary: A web app for applying syntax highlighting to code using the Pygments library.
tags: python
title: Pygmentizr
---

I really like [Pygments][pyg]. It's a Python module for applying syntax highlighting to code in printed documents. I use it on this blog, and when I had to include code listings in my university coursework, I used it with the [Minted package][mint] in LaTeX.

But recently I've needed to generate standalone code listings that aren't part of a larger document. I was using the command-line each time, but to make it a little easier, I've written a small web app instead. Here's a screenshot:

![](/images/2015/pygmentizr.png)

I enter the code in the first box, select the language, and click the button. The HTML and rendered preview appear at the bottom of the page. Really simple.

The code is all [on GitHub][git], and below I'll explain why I wrote it.

<!-- summary -->

The script is nothing special. It's just a tweaked wrapper around the first three entries of Miguel Grinberg's excellent [Flask Mega-Tutorial][flask]. I'm also using [Bootstrap][boot], and there's a meta discussion here about how I'm embracing more third party libraries like this -- but that's a discussion for another time.

Thing is, there's already a [Pygments demo][demo] which is quite similar to this. So why did I write my own?

1.  **I can add my own lexers**. As part of my day job, I work with languages that aren't included in Pygments. For example, in the last fortnight, I've been working with [Cisco and Juniper router configuration][cisco]. I'm also midway through writing my own lexer for a language called [YANG][yang].

    I can't use these lexers in the demo, but it's trivially easy to add them to my script.

2.  **I can get inline styles directly.** I often have to paste HTML into places that don't allow external stylesheets or `<style>` tags, but don't filter out inline styles. It's easy for me to add the flag which includes inline styles in my own script, but harder with the demo.

3.  **I can add my own post-processing.** CMSes have a tendency to mangle HTML in unexpected ways. For example, stripping out the line breaks in `<pre>` tags so all your code runs onto a single line. Yuk.

    I'll be able to add the changes to work around this directly, and make it a single step process. If I was using the web demo, I'd have to take the HTML and pass it through another script first.

None of which is to say that the demo is bad - it's just not suited to my purposes. It's not surprising that a custom tool fits my needs better.

For all that programmers argue about text editors, we all seem to agree that syntax highlighting is a good thing. The colours highlight the structure of the code, which makes it much easier to skim and read. I'm hoping this tool lets me use it in a few more places.

[pyg]: http://pygments.org/
[mint]: https://github.com/gpoore/minted
[git]: https://github.com/alexwlchan/pygmentizr
[flask]: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
[demo]: http://pygments.org/demo/
[cisco]: https://github.com/nemith/pygments-routerlexers
[yang]: https://tools.ietf.org/html/rfc6020
[boot]: http://getbootstrap.com/
