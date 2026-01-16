---
layout: post
date: 2022-08-28 16:49:37 +00:00
title: Getting blink diffs for photos on the iPad
summary: The Darkroom app lets me instantly switch between photos, which is how I compare and review shots.
tags:
  - photography
  - ios
  - ipad
index:
  exclude: true
---

When I'm taking a photo, I like to take several shots every time.
This is pretty common photography advice: it means you're more likely to get at least one good shot.
But it also means my library is full of fuzzy or repetitive photos, and I like to clean them up.

When I'm reviewing my photos, I like to use ["blink diffs"][blink diffs].
You switch rapidly between two similar images, and the back-and-forth helps you spot the difference.
The name comes from astronomy, and astronomers would use this technique to spot moving objects in pictures of the night sky.
I do blink diffs between my similar shots, and I only keep the best one.

You can try a simple blink diff by tapping the image below: you'll switch between three slightly different shots of the same tram.

<script>
  /* Ideally I'd send multiple sizes of image in srcset, but that doesn't seem to update -- since these are only ~750kB total, I think it's okay. */
  function switchImages() {
    const image = document.getElementById("switchableImage");

    image.src = image.src.indexOf("P7160890") !== -1
      ? image.src.replace("P7160890", "P7160891")
      : image.src.indexOf("P7160891") !== -1
      ? image.src.replace("P7160891", "P7160889")
      : image.src.replace("P7160889", "P7160890");
  }
</script>

<noscript>
  (Sorry, this demo only works if you have JavaScript enabled.)
</noscript>

<figure style="width: 500px;">
  <img src="/images/2022/P7160890_2x.jpg" id="switchableImage" onclick="script:switchImages();" style="cursor: pointer;" alt="Two double-decker trams standing on tracks in a gallery space. The left-hand tram has a dark red and yellow livery, with an open-air upper deck, the number '85' and a destination board 'Christchurch'. The right-hand tram has an orange, red and cream livery, and the departure board 'Farme Cross / Bridgeton Cross'.">
  <figcaption>
    A couple of trams I saw on a recent visit to the <a href="https://www.tramway.co.uk/">Crich Tramway Museum</a>.
  </figcaption>
</figure>

If I'm using [the Photos app] on my Mac, I can switch between photos using the arrow keys -- but I don't really want to manage photos on a computer.
Sitting at my computer feels like work; sorting through photos is a more casual task.
For a long time, I've wanted to browse my photos from a comfy chair with my iPad -- it's the sort of task the iPad should be good at.

Unfortunately, the built-in Photos app doesn't have a way to do the instant switching that I want.

{%
  picture
  filename="ipad_photos.jpg"
  width="600"
  style="border: 0.5px solid #d4d3d4;"
  alt="Screenshot of the iPad photos app. The photo of the two trams takes up most of the screen, with a toolbar along the top and a carousel of small thumbnails along the bottom. The carousel images are all tall and narrow, and tightly scrunched together."
%}

If I want to move to the next photo, I can swipe left or right -- but this does a full-screen animation, where the current photo gets "pushed" off the screen by the new photo.
The motion and the delay makes it much harder to compare photos.

I could also select a photo using the carousel of thumbnails at the bottom of the screen, which does switch straight to the chosen photo -- but they're very small.
On my iPad, they're 21&nbsp;&times;&nbsp;42&nbsp;points, less than half the [recommended size for tap targets][hig] in Apple's Human Interface Guidelines.
I struggle to hit them reliably.

Then I heard about an app called [Darkroom], and in particular its [workflow for reviewing photos][workflow].
I liked it almost immediately, because it makes it much easier to switch between photos without an intermediate animation.
This is what it looks like:

{%
  picture
  filename="darkroom_photos.jpg"
  width="600"
  alt="Screenshot of the Darkroom photos app. The photo of the two trams takes up most of the screen, with toolbars along the left and right, and a carousel of square thumbnails up the left hand side. The selected thumbnail is shown with a red outline, and the thumbnails are bigger and wider-spaced than in the built-in app."
%}

There's a carousel of thumbnails down the left-hand side (where I already have a hand holding the iPad), and the thumbnails are much bigger -- almost 5x more space than in the built-in app.
If I tap a thumbnail, it instantly switches to that photo.

<!--
Photos app = 42 × 84 = 3528 pixels
Darkroom  132 × 132 = 17,424 pixels

17,424 / 3528 = 4.939

https://developer.apple.com/design/human-interface-guidelines/foundations/layout

> On touch screens, provide ample touch targets for interactive components. Maintain a minimum tappable area of 44x44 points for all controls.
 -->

This app has way more features that I have yet to explore, but this alone will make me a paid subscriber.
I'd actually been thinking of building this sort of instant-switching photo browser myself (and I had a very early prototype), but now I don't have to.

[blink diffs]: https://en.wikipedia.org/wiki/Blink_comparator
[the Photos app]: https://en.wikipedia.org/wiki/Apple_Photos
[hig]: https://developer.apple.com/design/human-interface-guidelines/foundations/layout#best-practices
[Darkroom]: https://darkroom.co
[workflow]: https://medium.com/@jasperhauser/manage-your-growing-darkroom-photo-library-with-flag-reject-77c9e1816ef2
