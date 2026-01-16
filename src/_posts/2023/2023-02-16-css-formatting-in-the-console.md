---
layout: post
date: 2023-02-16 10:58:09 +00:00
title: CSS formatting in the console
summary: Did you know you can use `%c` to format your `console.log` messages?
tags:
  - web development
  - javascript
---

I was poking around in Google Lens recently (which is Google's magical [reverse image lookup service][bulb]) and I was mildly surprised by what I saw in the developer tools console:

{%
  picture
  filename="google-lens-console.png"
  width="750"
  class="screenshot"
  alt="A screenshot of a reverse image lookup, with the developer tools open on the right-hand side. I've selected the console tab, with a message in large text: 'WARNING! Using this console may allow attackers to impersomate you and steal your information using an attack called Self-XSS. Do not enter or paste code that you don't understand'. The word 'WARNING!' is in red text on a yellow background for extra emphasis."
%}

Code that runs in the dev console can be very powerful, so I can understand why they want to stop people from pasting random code in here -- although it feels like a bigger issue on, say, your Gmail inbox, rather than image search.
I'd never heard the name [Self-XSS][self-xss] before, but it definitely happens, and trying to reduce it is no bad thing.

After I'd stared at it for a few moments, and thought "that's neat", I got to wondering: how are Google formatting these messages?
How are they making their text big and bold and red and yellow?
Having a way to make console messages stand out would be quite handy.

It turns out that if you include `%c` in your `console.log`, you can then pass CSS styles as extra arguments.
Here are a few examples:

{%
  picture
  filename="simple-console-examples.png"
  width="554"
  class="screenshot"
  alt="A screenshot of using console.log formatters. The first is `console.log('This is regular text')` to show a baseline. The second is `console.log('%cThis is red text', 'color: red;')` which gets printed red. The third is `console.log('%cThis is BIG TEXT', 'font-size: 2em;')`, which is printed noticeably larger than the previous two lines. The fourth and last is `console.log('%cThis is text on yellow', 'background: yellow;')` which gets printed on a yellow background."
%}

You can also include multiple `%c` specifiers, and multiple CSS snippets, to style different parts of your message differently:

{%
  picture
  filename="multi-console-example.png"
  width="554"
  class="screenshot"
  alt="A screenshot of using complex console.log formatters. The first is `console.log('I can %cshout%c and I can %cwhisper', 'font-size: 2em', 'font-size: 1em', 'font-size: 0.65em')`, which prints 'I can shout and I can whisper', but 'shout' and 'whisper' are big/small respectively. The second is `console.log('Things aren't %cblack% and %cwhite', 'color: black; background: white; border: 1px solid black;', 'color: black', 'color: white; background: black;')`, which prints 'Things aren’t black and white', with the words black/white coloured to match."
%}

This felt weird to me at first, but now I write this post I realise it's just the [`%`-style format strings from C][printf] which I've been using my entire career, and which appear in a bunch of other languages.
But I've always used `%`-substitutions for values, never styles.
That's what feels new.

I'm not sure I'd use this for production code, but I can imagine it'd be useful for debugging.
I make heavy use of `console.log()`, and being able to highlight particular values would help me find them that bit faster (especially if it's a chatty site).

This doesn't work everywhere, but it does seem to work in the major browsers, and there's [documentation for it on MDN][mdn].

A few years ago, at a JavaScript meetup, I made a joke that *"my web development knowledge starts and ends with `console.log`"*.
On days like today, it's clear that I still have more to learn.

[mdn]: https://developer.mozilla.org/en-US/docs/Web/API/console#styling_console_output
[bulb]: /2023/changing-the-bulb-in-a-meridian-lighting-cir100b-ceiling-light/
[self-xss]: https://en.wikipedia.org/wiki/Self-XSS
[printf]: https://en.wikipedia.org/wiki/Printf_format_string
