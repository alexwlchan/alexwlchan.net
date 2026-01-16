---
layout: til
date: 2024-03-28 06:51:55 +00:00
title: Why is Pillow rotating my image when I save it?
summary: Images can have orientation specified in their EXIF metadata, which isn't preserved when you open and save an image with Pillow.
tags:
  - images
  - python
---
I was [having an issue][issue] where an image I'd exported from my Photos Library was being rotated when I opened and saved it:

```python
from PIL import Image  # pip install Pillow==10.1.0

im = Image.open("cross_stitch.jpg")
im.save("cross_stitch_saved.jpg")
```

The original image had a portrait orientation, but when I saved it the new image had a landscape orientation.
How?

After a bit of Googling and head scratching, I found [a comment from Andrew Murray in the Pillow repo][comment] where he mentioned a possible reason:

> I would imagine that the images you are dealing with have an EXIF orientation tag.
> This means that the image data is saved in one position, and then the image instructs the viewer to rotate it another way.

And indeed, when I opened the failing image in Preview.app and poked around in the metadata, I found a line that suggested this was the case:

```
Orientation: 6 (Rotated 90°C CCW)
```

There are two ways to ensure the orientation is preserved when I open and save with Pillow:

1.  Use Pillow to "bake in" the rotation, where you apply the transformation to the pixels:

    ```python
    from PIL import Image, ImageOps

    im = Image.open("cross_stitch")
    im = ImageOps.exif_transpose(im)
    im.save("cross_stitch_saved.jpg")
    ```
    
    This is what I did for my issue, because I didn't care about any of the EXIF metadata.

2.  Copy the EXIF data into the new photo:

    ```python
    from PIL import Image

    im = Image.open("cross_stitch.jpg")
    im.save("cross_stitch_saved.jpg", exif=im._exif)
    ```
    
    I'm not sure if this is the right way to copy EXIF in Pillow, because of the underscore on the attribute.
    It seemed to work in a quick test as I was writing this TIL, but I'd want to look more carefully if I really wanted to preserve the EXIF.

## The image dimensions were a clue

I was trying to write a regression test for this issue that checked the image dimensions were preserved upon saving -- because if the image is rotated, the dimensions must have changed: 

```python
from PIL import Image

im = Image.open("cross_stitch.jpg")
im.save("cross_stitch_saved.jpg")

saved_im = Image.open("cross_stitch_saved.jpg")

assert im.size == saved_im.size
```

I was surprised when this test passed before I'd fixed the rotation bug!

But the before/after dimensions were the same -- 4032&nbsp;×&nbsp;3024, which should have been more of a clue.
When I opened the image in Preview.app, it was a portrait photo, but those are landscape dimensions!
It was a clue that the raw pixel data didn't match what was being displayed, but I didn't realise it was significant until after I'd found the underlying issue.

[issue]: https://github.com/alexwlchan/scripts/pull/22
[comment]: https://github.com/python-pillow/Pillow/issues/4703#issuecomment-645219973
