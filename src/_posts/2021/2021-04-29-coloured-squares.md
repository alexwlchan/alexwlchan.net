---
layout: post
date: 2021-04-29 09:02:12 +0000
title: Drawing coloured squares/text in my terminal with Python
summary:
tags: python terminal-stuff colour
---

Last night, I [posted a tweet][tweet] wondering about the different colours of the ["spool of thread" emoji][emoji], and I made an illustration to show the variety:

<img src="/images/2021/emoji_1x.png" srcset="/images/2021/emoji_1x.png 1x, /images/2021/emoji_2x.png 2x" style="border-radius: 6px; width: 587px;" alt="A collection of different thread emojis, labelled by the platform/company they’re from. There are four red spools on the left, two blue spools on the right, a purple and two pink spools along the top, and a green spool along the bottom.">

The emoji icons are from [Emojipedia], and I've labelled each one with the name of the platform it comes from.
Notice that I've colour-matched each label to the emoji, and it's a different colour for each label -- how did I pick the colours?

I already have code [to extract dominant colours from images][dominant_colours], using *k*-means clustering.
I was able to use the script from the end of that post to get a list of suggestions:

<img src="/images/2021/terminal_without_colours.png" style="border-radius: 6px; width: 587px;" alt="A terminal window running a Python script that prints five hex colours.">

Problem is, I can't visualise colours from their hex codes.
Which colour is the murky brown, and which is the vibrant pink?
Wouldn't it be nicer if I could *see* the colours?

I found a [Perl function] that prints coloured blocks to the terminal using [ANSI escape codes].
I rewrote it in Python, and then I could see the hex code and the colour it represented:

<img src="/images/2021/terminal_with_colours.png" style="border-radius: 6px; width: 587px;" alt="A terminal window running a Python script that prints five hex colours, and a solid block of colour to the left of each code.">

Here's my Python function:

```python
def coloured_square(hex_string):
    """
    Returns a coloured square that you can print to a terminal.
    """
    hex_string = hex_string.strip("#")
    assert len(hex_string) == 6
    red = int(hex_string[:2], 16)
    green = int(hex_string[2:4], 16)
    blue = int(hex_string[4:6], 16)

    return f"\033[48:2::{red}:{green}:{blue}m \033[49m"
```

The function returns a string that prints a single coloured square, which you can use and print like any other string.
This won't work in every terminal app, but it works in the one I use (iTerm2), and that's good enough for my needs.

I don't fully understand ANSI escape codes, but reading the [Wikipedia entry] while writing this post helped me understand what's going on.
The `\033[…m` marks the escape code, and `48:2::r:g:b` sets the background colour of the terminal.
Typing a single space draws the square of colour, and then `49` restores the default background colour.

Scrolling up on that page, I see that `38:2::r:g:b` lets you set the foreground colour, and that lets me write another interesting function:

```python
def coloured_string(s, *, hex_string):
    """
    Returns a coloured string that you can print to a terminal.
    """
    hex_string = hex_string.strip("#")
    assert len(hex_string) == 6
    red = int(hex_string[:2], 16)
    green = int(hex_string[2:4], 16)
    blue = int(hex_string[4:6], 16)

    return f"\033[38:2::{red}:{green}:{blue}m{s}\033[39m"
```

Notice that the result now ends `39` to restore the default foreground colour, not `49`.
I got that wrong on my first attempt!

Combine this with something like [Unicode block elements], and this could be a very powerful tool.
For example, I can use a lower seven-eights block to add a gap between squares, and colour the hex swatches to match:

<img src="/images/2021/terminal_with_coloured_text.png" style="border-radius: 6px; width: 587px;" alt="A terminal window running a Python script that prints five hex colours, and a solid block of colour to the left of each code. The hex codes have the same colour as the blocks.">

This is even more useful -- it makes it visually obvious that, for example, the last colour would be unsuitable for text on a white background.

All this might seem like overkill for a throwaway tweet, but I'm bound to use it in other places.
Now I've done this, I have two functions that I can drop into any project that involves colours – and unlike a library, I completely understand how they work.
Writing blog post was a key part of that understanding – by explaining it to you, I first have to explain it to myself.

Being able to see colours in my terminal has been a "wouldn't it be nice if" debugging idea for a while, but I've never got round to it before.
Now I have, it's a single copy/paste to start reaping the benefits, so I'm much more likely to do it -- and maybe you will too.

[tweet]: https://twitter.com/alexwlchan/status/1387544124807593989
[emoji]: https://emojipedia.org/thread/
[Emojipedia]: https://emojipedia.org/thread/
[dominant_colours]: /2019/08/finding-tint-colours-with-k-means/
[Perl function]: https://unix.stackexchange.com/a/482782/43183
[ANSI escape codes]: https://en.wikipedia.org/wiki/ANSI_escape_code
[Wikipedia entry]: https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
[Unicode block elements]: https://en.wikipedia.org/wiki/Block_Elements
