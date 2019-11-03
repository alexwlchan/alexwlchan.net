---
category: Python
date: 2015-11-03 22:12:00 +0000
layout: post
link: http://www.bbc.co.uk/programmes/articles/4hVG2Br1W1LKCmw8nSm9WnQ/introducing-the-bbc-micro-bit
tags: python
title: Python and the BBC micro:bit
---

The BBC micro:bit is a tiny computer, intended for Year&nbsp;7 students to use to learn about programming (being distributed free to schools next spring).
It's the spiritual successor to the [BBC Micro](https://en.wikipedia.org/wiki/BBC_Micro).
Here's a picture from the BBC's website; it's about half the size of a credit card:

![A small black circuit board with a yellow and green stripe.](/images/2015/microbit.jpg)

One of the main programming languages on the micro:bit is Python, or rather [MicroPython](https://micropython.org), a version of Python 3 that's optimised for microcontrollers.
(The micro:bit has just 16K of RAM, so full Python is out of the question.)
I got to play with a micro:bit at tonight's meeting of [the Cambridge Python User Group](https://groups.google.com/forum/#!forum/campug), and it's a delightful piece of engineering.

For about an hour, we got to play with it &ndash; making the lights flash, trying the buttons, even playing music &ndash; and it's just *fun*.
Although there are only a handful of hardware features, there's a lot of scope for ideas &ndash; there were at least a dozen different ideas that came up tonight.
I particularly liked a mini-version of Snake and Pong played on the 5-by-5 screen, and some visualisations that played with the intensity of the LEDs.

There is something incredibly visceral about programming that enters the real world, having an effect beyond just text on a screen.

The software is equally remarkable.
It has a very robust, stable [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) built on MicroPython, and it works very well.
Inevitably, this isn't a complete implementation of Python 3 &ndash; 256K of storage puts a stop to that &ndash; but what it has seems very well done.
This isn't a dumbed-down or toy language.
It's proper Python, just with a smaller standard library.
I didn't have to think about it at all &ndash; I just used it like I would on any other computer.

I don't expect that everybody who uses this device will magically become a software developer, but I hope they have fun playing with it.

*Thanks to [Nicholas Tollervey](https://twitter.com/ntoll) for bringing the micro:bits for us to play with.*

*If you want to play with a micro:bit yourself, you should follow the [python-uk mailing list](https://mail.python.org/mailman/listinfo/python-uk).
There are going to be a handful more meetups/events with micro:bits before they all return to the BBC.
I'd highly recommend going if you have the chance!*