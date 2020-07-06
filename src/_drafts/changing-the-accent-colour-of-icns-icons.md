---
layout: post
title: Changing the accent colour of ICNS icons
summary: Playing with macOS ICNS image files to create new and interesting icons.
tags: images
---

One of my key tools is [nvALT], a notetaking app for macOS.
It's a fork of an older app called [Notational Velocity], and the icon is a greyscale version of the original:

<figure style="max-width: 500px;">
  <img alt="nvALT icon" src="/images/2020/nvalt.png" style="max-width: 49%; display: inline-block;">
  <img alt="Notational Velocity icon" src="/images/2020/notational.png" style="max-width: 49%; display: inline-block;">
  <figcaption>The icon of nvALT (left) and Notational Velocity (right).</figcaption>
</figure>

For a while now I've wanted to create versions of the Notational Velocity icon in different colours.
Adjusting the colour of an image with a single accent colour is [something I've done before](/2020/02/adjusting-the-dominant-colour-of-an-image/), and it would let me have something more exciting than a monochrome icon.
Given the renewed [sense of fun] in Apple's icons for macOS 11, I decided to see what I could do.

[nvALT]: https://brettterpstra.com/projects/nvalt/
[Notational Velocity]: http://notational.net/
[sense of fun]: https://applypixels.com/blog/comeback



## The structure of an icon

On macOS, icons can be displayed at a variety of sizes.
In Finder, an icon can range all the way from 16&times;16 to 512&times;512 pixels.
It's hard to draw a single version of an image that looks good in all these sizes, so macOS allows designers to draw multiple sizes of an icon.

Icons are stored in the [ICNS file format], which is a container with multiple images at different sizes.
When the OS needs to shows an icon at a given size, it picks the closest size from the ICNS file, and scales up or down as appropriate.
The big sizes can contain lots of detail, and the smaller sizes can be simplified so they remain clear.

For example, the Notational Velocity icon comes in six sizes:

<img src="/images/2020/notational-icon-sizes.png">

Notice how the 32&times;32 and 16&times;16 sizes have a different shape, doing away with the text sheets.
This allows the rocket shape to remain clear, even at a tiny size.

If you want to edit an ICNS file, you need to edit all of these sizes separately, then combine them back into a single ICNS.
You can edit ICNS images in Preview.app, but this is a manual process that involves lots of pointing and clicking.
I wanted to find other ways to do it.

(Icons on Windows are similar -- they use the [ICO format], which can also contain multiple images at different sizes.
Apps on iOS use PNG icons, with one file per size.)

[ICNS file format]: https://en.wikipedia.org/wiki/ICNS
[ICO format]: https://en.wikipedia.org/wiki/ICO_(file_format)



## Playing with Pillow

When I'm working with images, I often reach for [Pillow], the Python imaging library.
I've used it for several projects, and there are [old blog posts][pillow_posts] that explain those projects in more detail.

Pillow supports [ICNS files][pillow_icns], but it's a bit awkward -- it wants to work with one image at a time, and the "multiple sizes in one file" model of ICNS is a poor fit.
I got it working, but the code's not especially easy to follow.

I started writing about how to work with ICNS files in Pillow, and it got quite complicated for what felt like a simple task.
I remembered the [Zen of Python][zen]: *"If the implementation is hard to explain, it's a bad idea"*, and I went back to the drawing board.

[Pillow]: https://pillow.readthedocs.io/
[pillow_posts]: /all-posts-by-tag/#python-pillow
[pillow_icns]: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=icns#icns
[zen]: https://www.python.org/dev/peps/pep-0020/



## Investigating iconutil and ImageMagick

I looked at the [Pillow implementation of ICNS], and discovered that it shells out to a command-line tool called [`iconutil`](/files/2020/iconutil.html).
This is a macOS utility which works with ICNS files, allowing you to convert an ICNS file into a folder of images (an "iconset") and vice versa.
It's how developers are meant to create icons for their apps.

Here's an example:

```console
$ iconutil --convert iconset --output Notality.iconset Notality.icns

$ ls Notality.iconset/
icon_128x128.png icon_256x256.png icon_48x48.png
icon_16x16.png   icon_32x32.png   icon_512x512.png

$ iconutil --convert icns --output Notality2.icns Notality.iconset/
```

There are all sorts of tools that can operate on individual PNG images, and since I'm on the command line already I decided to try [ImageMagick].
The ImageMagick docs have a page describing [lots of ways to modify image colours][modifications], and I discovered the previously unknown-to-me `-modulate` flag.
This allows you to modify an image in the [HSL colour space][HSL colour space] (hue, saturation, lightness).

One of the examples of the `-modulate` flag shows an image of a red rose being cycled to different colours.
I can do the same thing with the Notational Velocity icon:

```console
$ magick Notality.iconset/icon_512x512.png -modulate 100,100,0 Notality.iconset/icon_512x512_cyan.png
```

Here's the result:

<figure style="max-width: 500px;">
  <img src="/images/2020/notational.png" style="max-width: 49%; display: inline-block;">
  <img src="/images/2020/notational_cyan.png" style="max-width: 49%; display: inline-block;">
  <figcaption>The Notational Velocity icon before (left) and after (right) having the <code>&#8209;modulate&nbsp;100,100,0</code> transformation applied.</figcaption>
</figure>

If I run this transformation over every PNG image in the iconset, then rejoin them back into an ICNS file, I'll have my hue-adjusted icon.

Here's what that looks like:

```bash
#!/usr/bin/env bash

set -o errexit
set -o nounset

# Apply an ImageMagick -modulate transformation to every size of an ICNS image.
#
#   $1 - path to the ICNS to transform
#   $2 - argument for the ImageMagick `-modulate` flag
#
function modulate_icns() {
    icns_path="$1"
    modulate_arg="$2"

    # Get the filename, filename before extension
    # https://stackoverflow.com/a/965072/1558022
    filename=$(basename "$icns_path")
    icon_name="${filename%.*}"

    iconset_path="$icon_name.iconset"
    out_path="$icon_name-$modulate_arg.icns"

    # Unpack the ICNS as individual images
    iconutil --convert iconset --output "$iconset_path" "$icns_path"

    # Apply the -modulate transformation to every individual image
    find "$iconset_path" -type f -exec magick '{}' -modulate "$modulate_arg" '{}' \;

    # Join the images back together into a single ICNS file
    iconutil --convert icns --output "$out_path" "$iconset_path"
}

modulate_icns "Notality.icns" "100,100,0"
```

I can combine that with a bash `for` loop to get the icon adjusted to a variety of colours:

```bash
for (( hue_rotate=0; hue_rotate<200; hue_rotate++ ))
do
  modulate_icns "Notality.icns" "100,100,$hue_rotate"
done
```

And voila, I have a rainbow of rocket icons:

<img alt="A grid of multi-coloured Notational Velocity icons" src="/images/2020/notality_rainbow_big.png">

And because it edited every size of the ICNS file, I get the same colours in the small icons as well:

<img alt="A grid of multi-coloured small Notational Velocity icons" src="/images/2020/notality_rainbow_small.png">

Look at all that colour!


[Pillow implementation of ICNS]: https://github.com/python-pillow/Pillow/blob/74a4c88a12737fd351797c137d8ade92c63b64b0/src/PIL/IcnsImagePlugin.py#L305-L312
[ImageMagick]: https://en.wikipedia.org/wiki/ImageMagick
[modifications]: https://www.imagemagick.org/Usage/color_mods/#modulate
[HSL colour space]: https://en.wikipedia.org/wiki/HSL_and_HSV



## Closing thoughts

To apply the icons, I open the "Get Info" panel in Finder for an app, then I drag the ICNS file over the icon preview.
On the Mac I'm writing this on, I have a blue icon that matches my Desktop wallpaper:

<img alt="The nvALT Dock icon with a blue rocket set against a blue background" src="/images/2020/nvalt_blue_screenshot.png" style="width: 450px;">

When I was younger, I spent a lot of time choosing and customising my icons.
That gradually dropped off and eventually I didn't have any custom icons.
I'm not about to go back to a hand-picked icon set, but it's nice to dip my toes (cliche) back in the water.
