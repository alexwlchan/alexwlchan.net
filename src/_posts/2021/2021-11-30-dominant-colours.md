---
layout: post
date: 2021-11-30 09:30:01 +0000
title: dominant_colours, a CLI tool for finding dominant colours in an image
summary: A new tool for playing with images.
tags:
  - images
  - colour
  - rust
  - my tools
colors:
  index_light: "#4576bb"
  index_dark:  "#88a7d3"
index:
  feature: true
---

At the weekend, I published [dominant_colours], a command-line tool for finding the dominant colours of an image.
It prints their hex codes to the terminal, along with a preview of the colour (in terminals that support ANSI escape codes).
For example:

<style>
  @media screen and (min-width: 500px) {
    #lighthouse_example {
      display: grid;
      grid-template-columns: 150px auto;
      grid-gap: 1em;
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

You can read [the README on GitHub][dominant_colours] to learn how to install it and how to use it.
In this post, I'll explain how and why I wrote it.



## Why did I write this?

I started thinking about dominant colours several years ago, when I wrote [Getting a tint colour from an image with Python and *k*-means][kmeans].

It works pretty well, and I started using it in a bunch of projects -- and for each new project, I'd copy and paste the code.
Different copies started to diverge as I tweaked and optimised them, and I no longer had a canonical implementation of this idea.

I wanted to get back to a single implementation, so that I could put all my ideas in one place -- rather than having them spread over multiple projects.

I also wanted it to be faster.
I use this code in a bunch of interactive scripts, and the old implementation took a second or so to run.
That may not seem like much, but it gets noticeable if you have to wait for it regularly.



## How does it work?

dominant_colours is written in Rust.

The heavy lifting is done by [Collyn O'Kane's kmeans-colors project][kmeans_lib], which includes a generic *k*-means library.
I did consider using the CLI tool that's part of the project, but it has lots of features I wouldn't use.
I wrote dominant_colours with the ["do one thing and do it well"][do_one_thing] mantra in mind.

I downsize all the images to be within 400&times;400&nbsp;pixels before passing them to the *k*-means process.
This makes the whole process much faster, because there are less pixels to deal with -- and it doesn't have much effect on the result.
If a colour was only visible in a fine detail that got lost in scaling, it probably wasn't a dominant colour.

Similarly, if I've got an animated GIF, I only take a sample of the frames, which are each in turn downsized to 100&times;100.
This dramatically reduces the number of pixels I have to deal with.
(The biggest GIF I have saved locally is 720&times;1019 and has 650 frames -- nearly half a billion pixels.
Sampling and resizing reduces that to a much more managable 350k pixels.)

I've wrapped the *k*-means process in a command-line interface created with [clap].
There's one argument and one flag which get used to configure the *k*-means process.

To draw arbitrary colours in the terminal, I'm using ANSI escape codes, adapting some Python from [another blog post I've written][ansi].



## Why did I pick Rust?

I've been increasingly picking Rust for small, standalone, interactive tools -- command-line applications that do all their work locally.
Rust binaries can be much faster than Python (the language I'd otherwise use), and for interactive stuff I really notice the difference.

I did some informal benchmarks of dominant_colours -- for even moderately sized images, it only takes a fraction of a second.
By comparison, Python takes at least a second for even the smallest image.
This difference is really noticeable -- a process that completes in a tenth of a second feels instant; a process that takes a second or more is a perceptible delay.

I'm not yet using Rust for anything that involves the Internet, because the network latency negates a lot of that speed benefit.
If I'm waiting multiple seconds for a remote server to give a response, I won't notice if I shave off half a second on my end.

As I was writing Rust, I was struck by the quality of the compiler errors.
The Rust compiler is very picky and I regularly had compiler errors, but they were super helpful in explaining what I should do next.
It feels like these errors get better each time I go back to Rust.
(For more on this, I recommend [Esteban Küber's talk at RustConf 2020][esteban].)

This approach to error checking permeates other parts of the Rust ecosystem.
This is the error you get from Clap if you misspell an argument:

<pre class="language-console">
<code><span class="gp">$</span> dominant_colours lighthouse.jpg --max-colors=3</code>
<code><span class="go"><span class="rustc_error">error:</span> Found argument '<span class="rustc_value">--max-colors</span>' which wasn't expected, or isn't valid in this context
      Did you mean <span class="rustc_warning">--max-colours</span>?

USAGE:
    dominant_colours &lt;PATH&gt; --max-colours &lt;MAX-COLOURS&gt;

For more information try --help</span></code></pre>

That's more helpful than any other tool I've seen, and it's the default behaviour in Clap.
I didn't have to opt-in or do anything special; I didn't realise it was there until I made a genuine typo.
This focus on UX and error handling means I'm more likely to use Rust and Clap in my next project.



## What's next?

I'm replacing all my Python implementations of *k*-means for dominant colours with this tool.

After that, this tool is probably done.
I don't want any more features, and I'm not aware of any bugs, so don't expect to see a lot of work on it in the future.
It's one of the nice things about writing small, single-purpose tools: you can finish them.

[dominant_colours]: https://github.com/alexwlchan/dominant_colours
[kmeans]: /2019/finding-tint-colours-with-k-means/
[kmeans_lib]: https://github.com/okaneco/kmeans-colors
[do_one_thing]: https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well
[clap]: https://crates.io/crates/clap
[ansi]: /2021/coloured-squares/
[esteban]: https://www.youtube.com/watch?v=Z6X7Ada0ugE
