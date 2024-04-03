---
layout: post
title: Toying with text truncation techniques
summary: 
tags: 
---

A while back I encountered a paper cut on my Apple Watch.
I opened Notification Centre, and it told me that I didn't have any notifications – but the message didn't quite fit on the screen.
The phrase "No Notifications" had been clipped and replaced with an ellipsis:
{%
  picture
  filename="apple-watch-no-notificati.png"
  width="162px"
  alt="A screenshot of an Apple Watch screen saying 'No Notificati...', where the word 'Notifications' has been truncated – but there's still space on the screen."
  class="screenshot dark_aware"
%}

This felt a bit sloppy – I don't think you need to clip the text.
There's plenty of spare horizontal space, and there are only a few characters left.
It feels like you could fit the whole phrase on screen.

It's easy to criticise, but harder to better.
Ever since I saw this screen, I've been wondering how I might do a "nicer" text truncation – and recently I got a chance to try it.
I was building an interface that shows some user-written text, but if it's too long, it needs to be clipped.
I'm not trying to fit under an exact character count, but I do want to avoid the text overwhelming the UI.

Here are a few of my ideas.

## The basic version

This is the simplest version, which just cuts the text when it passes a certain length:

```python
from typing import TypedDict


class TruncationResult(TypedDict):
    text: str
    truncated: bool


def truncate_text(text: str) -> TruncationResult:
    # Don't allow any text more than 180 characters
    if len(text) > 180:
        return {"text": text[:180], "truncated": True}
    else:
        return {"text": text, "truncated": False}
```

This isn't ideal for my problem: the text I'm dealing with can include newlines

## Limiting the number of lines


but can I do better?
let's see

had to write some code for thsi recently
truncate a block of arbitrarily long (user-written) text
can include newlines

not trying to fit udner exact char count, but want to avoid it overwhelming interface

heuristic #1: split by lines, only take first N

heuristic #2: allow a bit of "slop"
if the target is N characters, truncate at N-20
e.g. 180, truncate after 120 chars
=> will always be a non-trivial amount of text behind the ellipsis

heuristic #3: truncate on word boundaries
always show full words, not halfway through
(what if german words? nvm)

heuristic #4: no orphan lines
https://en.wikipedia.org/wiki/Widows_and_orphans
