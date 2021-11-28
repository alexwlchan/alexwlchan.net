---
layout: post
title: dominant_colours, a CLI tool for finding dominant colours in an image
summary: How I wrote my tool for finding dominant colours.
tags: images colour rust
---

At the weekend, I published [dominant_colours], a command-line tool for finding the dominant colours of an image.
It prints their hex codes to the terminal, along with a preview of the colour (in terminals that support ANSI escape codes).
For example:

<style>
  @media screen and (min-width: 500px) {
    #lighthouse_example {
      display: grid;
      grid-template-columns: 150px auto;
    }

    #lighthouse_example img {
      grid-row-start: 1;
      grid-column-start: 1;
      grid-column-end: 1;
    }

    #lighthouse_example pre {
      grid-row-start: 1;
      grid-column-start: 2;
      grid-column-end: 2;
    }
  }
</style>

<div id="lighthouse_example">
  <img src="/images/2021/lighthouse.jpg" style="width: 150px;" alt="A photo of a red and white lighthouse set against a blue sky.">
  <pre><code>$ dominant_colours lighthouse.jpg</code>
<code style="color: #e9e4d7;">█ #e9e4d7</code>
<code style="color: #858b88;">█ #858b88</code>
<code style="color: #4576bb;">█ #4576bb</code>
<code style="color: #2c231b;">█ #2c231b</code>
<code style="color: #c53b4e;">█ #c53b4e</code></pre>
</div>

You can read [the README on GitHub][dominant_colours] to learn how to install and how to use it.
In this post, I'll talk a bit about how I wrote it.

## Motivation

I started thinking about dominant colours several years ago, when I wrote [Getting a tint colour from an image with Python and *k*-means][kmeans].

I works pretty well, and I started using it in a bunch of projects -- and for each new project, I'd copy/paste the code.
Different copies started to diverge as I tweaked and optimised the code, and I no longer had a canonical implementation of this idea.

Creating a single tool that other projects can invoke gets me back to a single implementation.

I also wanted it to be faster.
I use this code in a bunch of interactive scripts, and the Python implementation takes a second or so to run.
That may not seem like much, but it gets noticeable if you have to wait for it regularly.



## How it works

I wrote this tool in Rust.
(More on that below.)

The heavy lifting is done by [Collyn O'Kane's kmeans-colors project][kmeans_lib], which includes a generic *k*-means library.
I did consider using the CLI tool that's part of the project, but it has lots of features I wouldn't use.
I wrote dominant_colours with the ["do one thing and do it well"][do_one_thing] mantra in mind.

I've wrapped the *k*-means library in a command-line interface created with [clap].
There's one argument and one flag which get used to configure the *k*-means process.

To draw coloured text in the terminal, I'm using ANSI escape codes, adapting some Python from [another blog post I've written][ansi].



## Why Rust?

This is the fourth tool I've written in Rust.

I've been picking Rust for small, standalone, interactive tools -- command-line applications that do all their work locally.
Rust is much faster than Python (my default choice for new tools), and for interactive stuff I really notice the difference.
It takes more work upfront, but I no longer feel like I'm waiting for my code to run.
Running a compiled Rust binary seems practically instant.

I'm not using Rust for anything that involves the Internet, because the network latency negates a lot of that speed benefit.
If I'm waiting multiple seconds for a remote server to give a response, I won't notice if I shave off half a second on my end.

As I was writing Rust, I was struck by the quality of the compiler errors.
The Rust compiler is very picky and I regularly had compiler errors, but they were super helpful in explaining what I should do next.
It feels like these errors get better each time I go back to Rust.
(For more on this, I recommend [Esteban Küber's talk at RustConf 2020][esteban].)

This approach to error checking permeates other parts of the Rust ecosystem.
This is the error you get from Clap if you misspell an argument:

<div class="language-console highlighter-rouge">
<div class="highlight">
<pre class="highlight">
<code><span class="gp">$</span> dominant_colours lighthouse.jpg --max-colors=3</code>
<code><span class="go"><span style="font-weight: bold; color: #d01c11;">error:</span> Found argument '<span style="color: #d0a311;">--max-colors</span>' which wasn't expected, or isn't valid in this context
      Did you mean <span style="color: #11d01c">--max-colours</span>?

USAGE:
    dominant_colours &lt;PATH&gt; --max-colours &lt;MAX-COLOURS&gt;

For more information try --help</span></code></pre>
</div>
</div>

That's more helpful than any other tool I've seen, and it's the default behaviour if you use Clap.
I stumbled upon this by accident, and I'm incredibly impressed.
This focus on UX and error handling is likely to swing me towards Rust and Clap for more projects in future.



## Benchmarks

<style>
  tr td:nth-child(2) {
    text-align: center;
  }

  tr td:nth-child(3), tr td:nth-child(4), tr td:nth-child(5), tr td:nth-child(6) {
    text-align: right;
  }

  table {
    width: calc(100% - 40px);
    border-collapse: collapse;
    margin-top: 1em;
    margin-bottom: 1em;
    background-color: rgba(182,182,182,0.09);
    margin-left: 20px;
    margin-right: 20px;
  }

  th {
    border-top:    3px solid rgba(153,153,153,0.6);
    border-bottom: 1.5px solid rgba(153,153,153,0.6);
  }

  table tr:last-child td {
    border-bottom: 3px solid rgba(153,153,153,0.6);
  }

  td, th {
    padding: 5px;
  }

  tr td:nth-child(1), tr th:nth-child(1) {
    padding-left: 8px;
  }

  tr td:last-child, tr th:last-child {
    padding-right: 8px;
  }
</style>

One reason to use Rust was to get a faster tool -- I run this in a bunch of interactive scripts, and the latency of the Python version is noticeable.
It felt faster, but I wanted to see if that was actually true.
I compared the performance of various implementations with five images:

-   A solid green PNG, which I have for easy testing.
    I thought this would be fast because the *k*-means process should converge immediately.
-   PNG screenshots of my screen and a single image
-   A JPEG image showing a computer-generated mind map, with large areas of solid colour
-   A JPEG photo of two people, with no areas of solid colour

I ran these tests on my 2016 MacBook – a five-year old machine that was slow when it was new.

These are the results:

<table style="width: 100%;">
  <tr class="header">
    <th>image</th>
    <th>dimensions</th>
    <th>size</th>
    <th style="min-width: 123px;">Python</th>
    <th style="min-width: 123px;">Rust (debug)</th>
    <th style="min-width: 123px;">Rust (release)</th>
  </tr>
  <tr>
    <td style="padding-right: 10px;">PNG, solid green</td>
    <td>500 &times; 500</td>
    <td>5KB</td>
    <td>1.08s</td>
    <td>0.89s</td>
    <td>0.06s</td>
  </tr>
  <tr>
    <td>PNG, small screenshot</td>
    <td>1228 &times; 614&nbsp;</td>
    <td>72KB</td>
    <td>1.01s</td>
    <td>1.49s</td>
    <td>0.05s</td>
  </tr>
  <tr>
    <td>PNG, large screenshot</td>
    <td>2880 &times; 1800</td>
    <td>2MB</td>
    <td>0.94s</td>
    <td>9.06s</td>
    <td>0.18s</td>
  </tr>
  <tr>
    <td>JPEG, graphic</td>
    <td>800 &times; 786</td>
    <td>180KB</td>
    <td>1.28s</td>
    <td>1.61s</td>
    <td>0.17s</td>
  </tr>
  <tr>
    <td>JPEG, photo</td>
    <td>2500 &times; 4379</td>
    <td>2MB</td>
    <td>0.90s</td>
    <td>13.37s</td>
    <td>0.51s</td>
  </tr>
</table>

There aren't any big surprises here: the Rust version is much faster than Python, and bigger images take longer to process.

I am surprised by how much slower a debug build is in Rust.
It makes sense, it's just surprising.
I saw something in a library's documentation about certain image operations being slower in debug builds while I was writing this, but I can't find it now.

What these numbers don't convey is the *feel* of this speed.
A process that completes in a tenth of a second feels almost instant; you notice you're waiting for a process that takes a second or more.



## What's next

I'm replacing all my Python implementations of *k*-means for dominant colours with this tool.

After that, this tool is probably done.
One of the nice things about writing small, single-purpose tools is that you can finish them.
I don't want any more features, and I'm not aware of any bugs.

[dominant_colours]: https://github.com/alexwlchan/dominant_colours
[kmeans]: /2019/08/finding-tint-colours-with-k-means/
[kmeans_lib]: https://github.com/okaneco/kmeans-colors
[do_one_thing]: https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well
[clap]: https://crates.io/crates/clap
[ansi]: /2021/04/coloured-squares/
[esteban]: https://www.youtube.com/watch?v=Z6X7Ada0ugE
