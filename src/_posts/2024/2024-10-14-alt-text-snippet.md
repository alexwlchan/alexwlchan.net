---
layout: post
date: 2024-10-14 19:26:43 +00:00
title: Making alt text more visible
summary: |
  I wrote a JavaScript snippet that shows alt text below all of my images, so I can see when it's missing, and review it while I'm editing.
tags:
  - blogging about blogging
  - accessibility
  - javascript
---
I add alt text to every image on this site.
I have an automated check to remind me to add alt text before I publish the site, but that means alt text has often been an afterthought -- something I'd dash out at the very end of writing a post.
I wanted to give it more attention, and make it part of my editing workflow.

When I'm doing a local build of the site, I now add this JavaScript snippet to every page:

```html
<script>
  window.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("img").forEach(function(img) {
      img.parentElement.innerHTML +=
        img.getAttribute('alt') !== null
          ? `<div
               style="background: lime;
                      font-family: monospace;
                      color: black;
                      padding: 5px;">
               Alt text: ${img.getAttribute("alt")}
             </div>`
          : `<div
               style="background: red;
                      font-family: monospace;
                      color: white;
                      padding: 5px;">
               No alt text!
             </div>`;
    });
  });
</script>
```

Here's what it looks like on an image, before and after I added alt text:

{%
  picture
  filename="alt_text_labels.png"
  width="500"
  class="screenshot"
  alt="Two photos of a red car. On the left-hand side there's a label with a red background 'no alt text'; on the right-hand side there's a label with a green background that contains the alt text."
%}

This snippet will look for any `<img>` tags on the page, and check them for alt text.
If the image has alt text, it adds the text below the image on a green background.
If the image doesn't have alt text, it adds a warning below the image on a red background.

The snippet only gets included in the page if I'm doing a local build.
This means that I'm the only person who sees these labels -- they aren't shown on the live site.

These labels make the alt text more visible to me, and remind me to write the alt text as part of writing the article.
It also means that I can see the alt text when I'm editing the article.
Previously the alt text was only visible in my Markdown source files, so once written I'd never review it or get a chance to improve it.
This means that I'm spending more time on my alt text, I'm getting more practice at writing it, and hopefully it's improving as a result.

Although I use Jekyll to build my site, there's nothing Jekyll-specific about it.
You could use this snippet to add alt text labels to any site.
