---
layout: til
title: Manage MP3 metadata from iTunes with eyed3
date: 2024-01-12 06:38:34 +00:00
tags:
  - python
  - macos
  - python:eyeD3
---
I have a couple of scripts that manipulate metadata in my iTunes library with the [eyed3 library][eyed3].
The library isn't particularly well-documented; these are some notes on how iTunes features map into eyed3.

[eyed3]: https://pypi.org/project/eyed3/

## Details > Year

In iTunes, you can set a year for a track: `Get Info` > `Details` > `Year`.

To retrieve this value with eyed3:

```python
import eyed3  # 0.9.7

audiofile = eyed3.load("song.mp3")

print(audiofile.tag.getBestDate())
```

Note that although you get a nice string representation of the date entered in iTunes, the value returned by `getBestDate` is actually a [eyed3.core.Date] instance.
You need to stringify it to get the value entered in iTunes.

The [`getBestDate()` function][getBestDate] is inspecting several ID3 tags; the one set by iTunes is `tag.recording_date`.

To set this value with eyed3:

```python
import eyed3  # 0.9.7
from eyed3.core import Date

audiofile = eyed3.load("song.mp3")

audiofile.tag.recording_date = Date(year=2017)
audiofile.tag.save()
```

[eyed3.core.Date]: https://github.com/nicfit/eyeD3/blob/5108937485555c81ca992a4def7d74f860ee978d/eyed3/core.py#L246
[getBestDate]: https://github.com/nicfit/eyeD3/blob/5108937485555c81ca992a4def7d74f860ee978d/eyed3/id3/tag.py#L480

## Artwork

In iTunes, you can set one or image images as artwork for a track: `Get Info` > `Artwork`.

To retrieve these images with eyed3:

```python
import io

import eyed3  # 0.9.7
from PIL import Image

audiofile = eyed3.load("song.mp3")

for i, af_image in enumerate(audiofile.tag.images):
    im = Image.open(io.BytesIO(af_image.image_data))
    im.save(f'image-{i}.{im.format.lower()}')
    # image-0.jpg, image-1.png, ...
```

To store artwork with eyed3:

```python
import eyed3
from eyed3.id3.frames import ImageFrame
from PIL import Image

audiofile = eyed3.load("song.mp3")

artwork = "album-art.png"

audiofile.tag.images.set(
    ImageFrame.OTHER,
    img_data=open(artwork, "rb").read(),
    mime_type=Image.open(artwork).get_format_mimetype()
)

audiofile.tag.save()
```

Note that this [set() function][set] takes two optional parameters: `description` and `img_url`.

[set]: https://github.com/nicfit/eyeD3/blob/5108937485555c81ca992a4def7d74f860ee978d/eyed3/id3/tag.py#L1595
