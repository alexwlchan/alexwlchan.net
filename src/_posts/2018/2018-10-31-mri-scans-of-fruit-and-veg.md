---
layout: post
date: 2018-10-31T09:10:26.014Z
title: Peering through MRI scans of fruit and veg
summary: What do you see when you pass fruit and vegetables through an MRI scanner? And how many animated GIFs can you make?
tags:
  - drawing things
  - wellcome collection
canonical_url: https://stacks.wellcomecollection.org/peering-through-mri-scans-of-fruit-and-veg-part-1-a2e8b07bde6f
---
*I wrote this article while I was working at Wellcome Collection. It was originally published [on their Stacks blog](https://stacks.wellcomecollection.org/peering-through-mri-scans-of-fruit-and-veg-part-1-a2e8b07bde6f) under a CC BY 4.0 license, and is reposted here in accordance with that license.*

<p>Having a <a href="https://wellcomecollection.org/works">large image collection to play with</a> means we’ve never short of a good illustration. Recently, somebody used an image of an MRI scan of a pumpkin as the cover picture on an internal blog post. Pretty appropriate in the run-up to Halloween:</p>

<figure>
  {%
    picture
    filename="pfex6r2r.jpg"
    width="750"
    alt=""
  %}
  <figcaption>An MRI scan along the axis of a pumpkin. By Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/rb4sm6fd">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>It’s one of a <a href="https://wellcomecollection.org/works?query=creators%3A%22Alexandr+Khrapichev%2C+University+of+Oxford%22">series of MRI scans</a> of fruit and vegetables. All the images were created by Alexandr Khrapichev, from the University of Oxford.</p><p>An MRI scan is a way to look inside the human body when other types of scanner can’t be used. It’s painless, non-invasive, and can give very high-resolution images. Rather than using x-ray or ultrasound, it uses powerful magnets to affect the movement of water molecules. (Remember that humans are 70% water!) Those movements can be used to construct an image.</p><p>Often — as seen here — a single MRI scan takes multiple “slices”. Each slice is a single cross-section of the body, and taking different slices gives you a detailed impression of the body’s interior.</p><p>In images like this one, Khrapichev has taken slices of a fruit or vegetable, used colours to match the original, and then stitched them together into a single high-resolution image. It’s a bit of fun, and it nicely illustrates how an MRI scan works.</p><p>When I saw these images, I wanted to break them back into individual slices, and combine them into an animated GIF. For me at least, that works a lot better than seeing them laid out on a static page. Since these images are all licensed as CC BY, I’m okay to do that, as long as I link back to the originals!</p><p>I’ve been sharing a few examples <a href="https://twitter.com/alexwlchan">on my Twitter account</a>, but I wanted to give them a more permanent home. The full resolution images are gorgeous, and the compression on Twitter doesn’t do it justice.</p><p>In this post, I’ll show off some of my favourite images. In a sequel, I’ll explain the code I used to create them.</p><p>Let’s start with something quite familiar: an apple. Turning it into a GIF shows the shape of the apple, and we can see the gaps in the core:</p>

<figure>
  <img src="/images/2018/animated_fruit/1*0A1CEwcu9jXLh7l4WReFZA.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of a sagittal view of an apple. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/mwn9qf6m">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Here’s another pair of images which are really familiar: a mandarin and a lemon. Within the MRI, you can see the segments of the two citrus fruits — and the occasional flash of a seed.</p>

<figure>
  <img src="/images/2018/animated_fruit/1*J6_xF89Y6UqsuY0Ft6hc2g.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of an lemon. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/t2h4c4n3">Wellcome Collection</a>, CC BY. It’s hard to be sure, but I think this scan must start partway through the lemon — we don’t see it shrink at the ends.</figcaption>
</figure>

<figure>
  <img src="/images/2018/animated_fruit/1*Y6ZEP5NxeNJ-8RA7NbAi-Q.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of an orange. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/sxm89b3x">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>I love the vibrancy of the bright orange against the black background. The side view is equally impressive:</p>

<figure>
  <img src="/images/2018/animated_fruit/1*sw_sCusnQhbAz5zBey_GVQ.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of a sagittal view of an orange. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/semnhwc6">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>I’m also rather taken with the red in this tomato. I can see the aspects of a tomato when I look at it, but I don’t think it’s quite as recognisable.</p>

<figure>
  <img src="/images/2018/animated_fruit/1*NGUMEkAvlyqmQC43SpgCPw.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of a tomato. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/nmppywpm">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Turning towards the more unusual, this is a kiwifruit. Not only is it a pleasing shade of green, it also shows off the structure nicely. The core and the seeds really stand out in this image:</p>

<figure>
  <img src="/images/2018/animated_fruit/1*nMJOS6lMoxjFlVWGgW796g.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of a kiwfruit. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/aqzd3qh7">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Going for something even odder, this scan of a passion fruit looks closer to frog spawn than fruit — in fact, it’s the numerous seeds. Once you know what it is, it makes a lot more sense!</p>

<figure>
  <img src="/images/2018/animated_fruit/1*-lRkN1t4HKnm5tt7E6q6Iw.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of a passion fruit. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/xkn4pw2u">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Here’s another one which is quite unusual, and which I find almost mesmerising. It looks like something from the world of microbiology — a cluster of tiny cells — but it’s much larger. Can you guess what it is?</p>

<figure>
  <img src="/images/2018/animated_fruit/1*TRERlZijFg-iA9Xu3kCouA.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of… well, something. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/qbv99v5k">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Any ideas? If it helps, here’s another view of the same object, this time from a different angle:</p>

<figure>
  <img src="/images/2018/animated_fruit/1*aJuRWvqdag11FD-BU3ZLyw.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>A sagittal view of the same object. I can’t help but see animal faces peering at me from the dark, but maybe that’s just me… Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/vwp2yvdd">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Did you guess correctly?</p><p>This is garlic — each segment is an individual clove, which grows as we move from one end towards the centre, then tapers off again at the other end.</p><p>There are some even weirder ones. This axial view of a cabbage puts me in mind of the opening credits of <em>Doctor Who</em>. It’s almost hypnotic:</p>

<figure>
  <img src="/images/2018/animated_fruit/1*Fmpbt4SBWebr-S3L19KLxQ.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of a cabbage. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/rq48tke5">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>And the other view of the cabbage isn’t any less strange — like a sort of magical forest, the trees growing alongside the path to greet you.</p>

<figure>
  <img src="/images/2018/animated_fruit/1*5Ygqw2ZXPzsaY45dDBHQPg.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of a sagittal view of a cabbage. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/kgz34m4e">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Somehow, these images make cabbage seem much more interesting than when I had it for school dinners.</p><p>But what most surely be my favourite bizarre image is the artichoke. The collage image is a bit odd, but stitching them together looks like a portal opening in space. (Has anybody ever used images from an MRI in a science-fiction show?)</p>

<figure>
  <img src="/images/2018/animated_fruit/1*re6vsssoSzSnuvVMXqoOBw.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of a sagittal view of an artichoke. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/b9g485fs">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>And finally, to round out this post, here a GIF of the pumpkin I opened the post with:</p>

<figure>
  <img src="/images/2018/animated_fruit/1*khJavcBL8IB_j_JkFOpNqg.mp4" class="dark_aware" loading="lazy" style="aspect-ratio: 1;" alt="">
  <figcaption>Based on an MRI scan of an axial view of a pumpkin. Original images by Alexandr Khrapichev, University of Oxford. Source: <a href="https://wellcomecollection.org/works/rb4sm6fd">Wellcome Collection</a>, CC BY.</figcaption>
</figure>

<p>Happy Halloween!</p>
