---
layout: post
date: 2022-11-04 22:27:35 +00:00
title: A simple gallery plugin for Obsidian
summary: Making it easier to find all the images in my Obsidian vault.
tags:
  - obsidian
  - javascript
link: https://github.com/alexwlchan/obsidian-simple-gallery
colors:
  index_light: "#121212"
  index_dark:  "#ababab"
---

I've been using [Obsidian] for my note-taking recently, and I really like it.
It's already absorbed all of my text notes, and I'm gradually using it for images too.

To help me find my images, I've written a small Obsidian plugin.
When I click the little picture icon in the sidebar, it finds all the images in my vault, and displays them in a grid, like so:

{%
  picture
  filename="obsidian-screenshot.png"
  alt="An Obsidian window with a tab titled “Gallery” and four rows of images on a dark background. Each image is of fixed height but varying width, depending on the aspect ratio."
  width="750"
%}

There are [a few community plugins][community] for doing galleries, and they have more features and options – but they're also more complicated than what I wanted.
This is just a scrolling grid of images, and if you click on a thumbnail, it opens the full-sized image.

(If this design looks familiar, it's because it's based [on the new concepts page][concepts] my team have been building at work.)

When I'm looking at a full-sized image, if I want to see where it's used, I can click the "More options" menu in the upper right, and open the backlinks:

{%
  picture
  filename="obsidian-backlinks.png"
  alt="An Obsidian window titled ‘Backlinks for entity_and_resource_policies’, showing the full-sized image on the left-hand side, and a search result showing the single note where it’s used on the right."
  width="702"
%}

I started from [the Obsidian sample plugin][sample], and kept editing it until I had something I liked.
Because Obsidian is built using web tech, I was able to write the entire plugin using JavaScript and HTML that I already know.
The whole thing is a hundred lines, and it even works on my iPhone.

I don't have any plans to write more Obsidian plugins, but it's reassuring to know that I could.

I've put all the plugin code on GitHub -- I'm not sure anybody else wants it, but maybe reading my code might be useful if you want to write your own plugins.

[Obsidian]: https://obsidian.md/
[community]: https://obsidian.md/plugins?search=gallery
[concepts]: /images/2022/concepts-screenshot.png
[sample]: https://github.com/obsidianmd/obsidian-sample-plugin
