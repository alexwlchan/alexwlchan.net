---
layout: post
date: 2022-01-14 10:58:15 +0000
title: Creating animated GIFs from fruit and veg
summary: Some Python code for turning MRI scans of fruit and veg into animated GIFs.
tags: python drawing-things wellcome-collection
index:
  tint_color: "#5c5a30"
---

A couple of years ago, I wrote a blog post about [looking through MRI scans of fruit and veg][stacks].
I took some MRI scans by Alexandr Khrapichev from the University of Oxford, ran them through an image processor, and turned them into animated GIFs.
They're very pretty and mesmerising.

That post has dozens of examples, but my favourite is this view [of an artichoke][artichoke], which looks like some sort of portal from science fiction:

<script>
  function toggle() {
    var img = document.getElementById("artichoke");
    var toggleControl = document.getElementById("toggleControl");

    console.log(img.src);

    if (img.src.endsWith(".jpg")) {
      img.src = "/images/2022/artichoke.gif";
      toggleControl.innerHTML = "&#x23EF;&#xFE0E; pause";
    } else {
      img.src = "/images/2022/artichoke.jpg";
      toggleControl.innerHTML = "&#x23EF;&#xFE0E; play";
    }
  }
</script>

<figure>
  <img src="/images/2022/artichoke.gif" id="artichoke" style="width: 375px;" alt="An animated image showing a yellowy-green burst of vaguely circular lines moving outward (as we move to the middle of the artichoke), and then gradually collapsing in (as we move towards the end).">
  <center>
    <a href="#artichoke" onclick="script:toggle()" id="toggleControl">&#x23EF;&#xFE0E; pause</a>
  </center>
</figure>

At the time, I meant to write a follow up post explaining how I created these images, but I never got round to it.
I recently rediscovered the code while clearing up an old hard drive, so let's go through it now.
All of this code uses Python and the [Pillow] library, because those were my go-to tools for working with images when I wrote this code.

Khrapichev saved his scans as a single large image, with the individual scans arranged into rows and columns.
This is the image he published:

<figure>
  {%
    picture
    filename="artichoke_frames.jpg"
    alt="A grid of different views of the artichoke in yellow-green, arranged in rows and columns against a black background."
    visible_width="750px"
    link_to_original
  %}
  <figcaption>
    Artichoke, axial view, MRI.
    By <a href="https://wellcomecollection.org/works/b9g485fs">Alexandr Khrapichev, University of Oxford</a>.
    Used under CC BY 4.0.
  </figcaption>
</figure>

So we want to cut out the individual frames from this image, put them in the right order, then stitch them into an animated GIF.

First we load the image with Pillow:

```python
from PIL import Image

im = Image.open("artichoke.jpg")
```

We can crop a rectangle from an image using [the `crop()` function][crop_function], which takes the four corners of the area we want to crop.
For example, this code:

```python
im_cropped = im.crop((500, 1000, 800, 700))
```

will extract this part of the image:

{%
  picture
  filename="artichoke_frames_cropped.png"
  alt="The same grid of images as previously, but mostly dimmed and with only a small area in full colour and outlined with a red rectangle (highlighting the area to be cropped)."
  visible_width="500px"
%}

I started by writing a function that produces the 4-tuples that are passed to the `crop()` function.
It moves from left-to-right, top-to-bottom, finding the coordinates of the crops:

```python
def get_crops(im, *, columns, rows):
    column_width = im.width // columns
    row_height = im.height // rows

    for r in range(rows):
        for c in range(columns):
            x = c * column_width
            y = r * row_height
            yield (x, y, x + column_width, y + row_height)
```

and then I get the individual images like so:

```python
individual_scans = [
    im.crop(c)
    for c in get_crops(im, columns=7, rows=4)
]
```

The exact number of individual scans varied from image to image (for example, [the sagittal view of a pumpkin][pumpkin] has 6 columns and 3 rows), so parameterising the crops was quite handy.

{%
  picture
  filename="artichoke_crops.png"
  alt="The same grid of images as previously, but now split into individual images, separated by white borders."
  visible_width="500px"
%}

Now we save the individual frames as an animated GIF, which is [a one-liner in Pillow][save_gifs]:

```python
individual_scans[0].save(
    "artichoke.gif",
    save_all=True,
    append_images=individual_scans[1:]
)
```

It's possible to adjust the speed by passing a `duration` parameter, but the default seemed fine.
I'm sure there's more fun to be had by making the animation speed up or slow down at certain points!

You can download all the code from this post in this file:

{% download /files/2022/make_artichoke_gif.py %}

And if you haven't looked already, I really recommend getting a big monitor and reading [my original post][stacks].
There are pumpkins, parsimmons, passion fruit, and all sorts of other mesmerising images made entirely from MRI scans.

[stacks]: https://stacks.wellcomecollection.org/peering-through-mri-scans-of-fruit-and-veg-part-1-a2e8b07bde6f
[artichoke]: https://wellcomecollection.org/works/b9g485fs
[Pillow]: https://pypi.org/project/Pillow/
[collection]: https://wellcomecollection.org/works/b9g485fs
[crop_function]: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.crop
[pumpkin]: https://wellcomecollection.org/works/z3cja6w4
[save_gifs]: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=gif#saving
