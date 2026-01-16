---
layout: post
date: 2022-05-07 19:28:31 +00:00
title: Find the dominant colours in an image in your web browser
summary: Wrapping my CLI tool for finding dominant colours in a lightweight web app.
tags:
  - colour
  - glitch
  - fun stuff
link: https://dominant-colours.glitch.me/

colors:
  index_light: "#1b3055"
  index_dark:  "#bdbdc2"
---

Last year, I created [a CLI tool][cli] for finding the dominant colours in an image.
It's been super useful and I use it multiple times a week, but I can only use it when I have access to a command-line -- and sometimes I want to use it on my phone, where I don't.

I've wrapped the CLI tool in a small web app, which lets you upload images to analyse:

{%
  picture
  filename="dominant_colours_landing.png"
  alt="Screenshot of a web page titled 'find the dominant colours in an image', with a button to upload a file and a submit button."
  width="484"
%}

and then it shows you a palette of the dominant colours:

{%
  picture
  filename="dominant_colours_screenshot.png"
  alt="A screenshot of the web app. It says 'find the dominant colours in an image' in bold letters at the top, then an illustration of two people in a Chinese dragon costume. On the right hand side are the dominant colours from that image: brown, blue, red and yellow, along with hex codes. At the bottom is a red-coloured link 'try another image'."
  width="484"
%}

The CLI tool allows you to pick the size of the palette, whereas the web app always returns five colours.
I might add that at some point, but it felt a non-trivial design challenge to add a option to the first page, describe it in a sensible way, and have the palette continue to look good with a variable number of colours.
This works as a 1.0.

It was pretty easy to wrap this in a web app, which is part of why I made the CLI tool in the first place -- I'd written this sort of dominant colours algorithm a bunch of times, and I wanted a single canonical implementation I could reuse.
The web app just shells out to the CLI tool for the image analysis (after [recompiling to run in Glitch][recompiling]).

If you'd like to try it, it's available at <https://dominant-colours.glitch.me/>

If you want to read the source code, it's [on GitHub][github].

[cli]: /2021/dominant-colours/
[recompiling]: /2022/rust-on-glitch/
[github]: https://github.com/alexwlchan/dominant_colours/tree/main/webapp
