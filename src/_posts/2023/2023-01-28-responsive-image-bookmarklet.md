---
layout: post
date: 2023-01-28 10:30:50 +00:00
title: A bookmarklet to show which responsive image was chosen
summary: "Debugging my &lt;picture> and &lt;source> tags."
tags:
  - blogging about blogging
  - images
  - web development
---

I've had a lot of fun fiddling with the images on this blog recently, and I think they're better than when I started.
I've read a bunch of articles on responsive images, and I've sprinkled the [`<picture>`][picture] and [`<source>`][source] tags everywhere to offer images in a variety of sizes and formats.
  
If you're using a device with a small screen, you'll get a small image that doesn't waste data.
If you're using a device with a big screen, you'll get a big image that looks sharp and crisp.
If you're using dark mode, you'll get an image that isn't blindingly white.
That's the theory, anyway.

I've written a small bookmarklet which adds a label to show me which version of an image the browser has chosen -- this helps me check I've got my image markup correct.
Here's the code:

```javascript
/* Given the currentSrc attribute of an image, get a label.
 *
 * Ideally this should be something which identifies the image,
 * e.g. my different sizes are named cat_1x.jpg, cat_2x.webp, cat_3x.avif,
 * so it gets everything after the last underscore.
 */
function createLabel(currentSrc) {
  return currentSrc.split('_')[currentSrc.split('_').length - 1];
}

/* Remove any previously-added labels */
document
  .querySelectorAll('.pictureSourceOverlay')
  .forEach(pso => pso.remove());

document
  .querySelectorAll('img')
  .forEach(img => {
    const div = document.createElement('div');
    div.innerHTML = createLabel(img.currentSrc);
    div.style.position = 'absolute';
    div.style.zIndex = 10;
    div.classList.add('pictureSourceOverlay');

    div.style.background = 'white';
    div.style.fontFamily = 'monospace';
    div.style.fontSize   = '1em';
    div.style.lineHeight = '1.3em';
    div.style.color      = 'green';
    div.style.marginTop  = '10px';
    div.style.marginLeft = '10px';
    div.style.padding    = '2px 10px';

    img.parentNode.insertBefore(div, img.previousSibling);
  });
```

I've packaged this up with [Peter Coles' bookmarklet creator][coles], and when I run it on a page, I get a little label in the top left-hand corner of each image, showing me what the browser has selected:

{%
  picture
  filename="image-label-bookmarklet.jpg"
  width="567"
  class="screenshot"
  alt="A screenshot of a blog post, with three images inline with the text. Each image has a small label in the top left-hand corner, green text on a white background, saying “2x.webp”."
%}

This is tuned for my site and the way I name images; the general idea should work on other sites, but you may need to tweak the `createLabel` function to get useful labels.

I can also find this info using the developer tools, but I found it easier to have it accessible in a bookmarklet I had bound to a keyboard shortcut.
  
[responsive]: https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
[picture]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture 
[source]: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/source
[coles]: https://mrcoles.com/bookmarklet/
