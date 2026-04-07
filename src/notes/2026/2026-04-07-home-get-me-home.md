---
layout: note
date: 2026-04-07T20:55:47Z
title: HOME_GET_ME_HOME is a Citymapper Shortcuts action
summary: It's a Citymapper action that gives directions to my home, which can be triggered using the Shortcuts app.
topic: Computers and code
---
The other day, I pulled up Spotlight on my iPhone, and I saw a Siri Suggestion I didn't recognise -- it suggested `HOME_GET_ME_HOME` with Citymapper, which looks like a programmer's variable name:

{%
  picture
  filename="home-get-me-home.png"
  width="562"
  class="screenshot"
  alt="Siri Suggestions, which show four apps along the top, a Kindle action to 'Play current', and a Citymapper action to 'HOME_GET_ME_HOME'."
%}

Maybe this is a variable name which has leaked, and there's meant to be some more user-friendly text here -- but the meaning is also pretty obvious to a non-programmer.

I did a bit of digging, and I found `HOME_GET_ME_HOME` as one of two Citymapper actions in the Shortcuts app, and it's an action to "Get directions to your saved home in Citymapper".
You can use it in a shortcut -- I imagine it might be useful for, say, a "leaving the office" shortcut which starts a playlist, texts your partner, and starts getting directions home.

More confusing is `HOME_GET_ME_TO_WORK`, an action to "Get directions to your saved work in Citymapper".

(I'm running Citymapper 11.40.1; who knows if this will change in a future version.)
