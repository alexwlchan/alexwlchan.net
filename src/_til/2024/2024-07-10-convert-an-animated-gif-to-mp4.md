---
layout: til
title: Convert an animated GIF to an MP4 with ffmpeg
date: 2024-07-10 22:30:08 +01:00
tags:
  - ffmpeg
---
I sometimes need to convert animated GIFs into MP4 movie files -- this can often result in much smaller files, which is useful for serving the images on the web.

This is the `ffmpeg` command I use:

{% code lang="shell" %}
ffmpeg \
  -i INPUT_GIF_PATH \
  -movflags faststart \
  -pix_fmt yuv420p \
  [-vf scale=WIDTH:HEIGHT] \
  [-y] \
  OUTPUT_MP4_PATH
{% endcode %}

Here's what it's doing:

*   `-i INPUT_GIF_PATH` is the path to the animated GIF I want to convert

*   `-movflags faststart` does something to move the metadata around in the file.
    I'm not sure what the benefit of this is; it's been in my copy/pasted version of this code for years.

*   `-pix_fmt yuv420p` is choosing a pixel format.
    I'm not entirely sure what this is doing of why `yuv420p` is the value I should be using, but if I omit it, the videos don't work in QuickTime Player or Safari.

*   `-vf scale=WIDTH:HEIGHT` set the dimensions of the final video.
    If I omit this, the MP4 is generated at the same dimensions as the original GIF.

    There's some subtlety to this I don't understand yet.
    I was converting a 600×660 GIF to a 363×400 MP4, and I got an error in the conversion process:

    ```
    width not divisible by 2 (363x400)
    ```

    According to [Stack Overflow](https://stackoverflow.com/a/20848224/1558022), this is because H.264 requires even dimensions.
    Tweaking the desired width so it was even seems to fix this.

*   `-y` tells ffmpeg to overwrite the existing file, if it already exists.
    If you don't provide this flag and the file already exists, it presents an interactive prompt:

    ```
    File 'out.mp4' already exists. Overwrite? [y/N]
    ```