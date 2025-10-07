---
layout: til
title: Don't show Dock icons from apps on another device
summary: |
  The name of this feature is "Handoff", and that's where you'll find the setting for it.
date: 2025-10-07 08:33:37 +0100
tags:
  - macos
colors:
  css_light: "#1a6cce"
  css_dark:  "#3aa5eb"
---
Every so often, an icon appears in my Dock offering to bring across windows or documents I have open on another Mac:

{%
  picture
  filename="dock_handoff.png"
  width="510"
  class="screenshot"
  alt="My Dock has two Safari icons – regular Safari, then one that’s annotated ‘Safari from Mac mini’."
%}

I find this quite frustrating, and I often click the wrong icon by accident and end up with a window I don't want.
There's also no way to dismiss these icons on a one-off basis.
Go away!

I looked in the Settings app under Dock, and I couldn't find a setting that controls this behaviour.
I also looked for Continuity (because that's a marketing name sometimes used for this feature), and finally found it under Handoff.

The setting I had to disable is *"Allow Handoff between this Mac and your iCloud devices"*.

When I disable it, I'm warned that this also disables moving my cursor and keyboard to a nearby Mac or iPad, and I think it might affect the shared clipboard too?
I'll see if I'm missing other features in the long run, but in the meantime I have a slightly more peaceful Dock.