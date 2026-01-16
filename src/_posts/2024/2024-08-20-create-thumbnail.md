---
layout: post
date: 2024-08-20 17:16:50 +00:00
title: "create_thumbnail: create smaller versions of images"
summary:
  I've made a new tool that allows me to reuse my thumbnailing code across all my projects.
tags:
  - rust
  - my tools
  - images
colors:
  index_light: "#697c13"
  index_dark:  "#b6b86c"
index:
  feature: true
---
I’ve made a new command-line tool: [create_thumbnail], which creates thumbnails of images.
I need image thumbnails in a lot of projects, and I wanted a single tool I could use in all of them rather than having multiple copies of the same code.

It takes three arguments:

*   Your original image;
*   The directory where you're storing thumbnails;
*   The max allowed height or width of the thumbnail you want.
    You constrain in one dimension, and it resizes the image to fit, preserving the aspect ratio of the original image.

The tool prints the path to the newly-created thumbnail.
Here are two examples:

```console
$ create_thumbnail clever_cat.jpg --out-dir=thumbnails --width=100
./thumbnails/clever_cat.jpg

$ create_thumbnail dappy_dog.png --out-dir=thumbnails --height=250
./thumbnails/dappy_dog.png
```

It supports JPEG, PNG, TIFF, WEBP, and both static and animated GIFs.
Thumbnails match the format of the original image, except for animated GIFs, which become MP4 movies.

## How does it work?

The heavy lifting is done by the [image crate] and [ffmpeg].

Here's how you can use the image crate to resize an image in Rust:

{% code lang="rust" names="0:image_path 1:thumbnail_path 2:width 3:height" %}
let image_path = "pineapple.jpg";
let thumbnail_path = "thumbnail.jpg";

let (width, height) = (306, 204);

image::open(image_path)?
    .resize(width, height, image::imageops::FilterType::Lanczos3)
    .save(thumbnail_path)?;
{% endcode %}

The documentation for the `resize()` method has [some good examples][resize] of the different filter options -- how they affect the quality of the image and the time taken to create it.
I'm using Lanczos with window 3 because it creates the best looking image (to my eyes at least), and I'm not particularly performance constrained.

Here's a shell script that uses ffmpeg to [create an MP4 video of an animated GIF](/til/2024/convert-an-animated-gif-to-mp4/):

{% code lang="shell" names="0:gif_path 1:thumbnail_path 2:width 3:height" %}
gif_path="animated_squares.gif"
thumbnail_path="animated_squares.mp4"

width="16"
height="16"

ffmpeg \
  -i "$gif_path" \
  -movflags faststart \
  -pix_fmt yuv420p \
  -vf "scale=$width:$height" \
  "$thumbnail_path"
{% endcode %}

My tool is a wrapper around these two snippets.
It picks the correct dimensions for the final thumbnail based on the dimensions of the original image and the max width/height, then runs these two snippets to create the thumbnail.

(This turns out to be not completely trivial: something in ffmpeg requires that the width/height be even numbers.
If you try to create a video with an odd width/height, the command fails to create anything.
This is something I've rediscovered multiple times, and now it's encoded in this tool.)

[create_thumbnail]: https://github.com/alexwlchan/create_thumbnail
[image crate]: https://crates.io/crates/image
[ffmpeg]: https://www.ffmpeg.org/
[resize]: https://docs.rs/image/0.25.2/image/imageops/enum.FilterType.html#examples

## Why did I make this?

I've written some version of a thumbnailer in at least a dozen projects.
There's only one variable that differs between them: how big are the thumbnails?
In one project I might want thumbnails that are 100 pixels wide, in another I need thumbnails that are no more than 250 pixels tall.
Although imaging libraries expose lots of options, the thumbnail dimensions are the only one that I change for each project.

This is what informed the design of my new tool: you can choose the width/height of the thumbnails it creates, but nothing else.
I take this approach with a lot of [my scripts and tools](https://github.com/alexwlchan/scripts): wrap a versatile, flexible interface with one that's more tightly constrained and exposes the few options I use.
I find this easier to use because I have less to remember on a day-to-day basis.

Creating a single, standalone tool means I can simplify all other these projects: they can just call my new tool, rather than having their own code for creating thumbnails.
It also makes it easier to keep these projects up-to-date, if I ever change my preferred options for the image crate or ffmpeg.

There's a popular ["rule of three"][three] that says if you write the same code three times, you should refactor it into a shared function.
I'm pretty good at following this rule within a single project, but not so much across multiple projects.
I should have created a standalone thumbnailer a long time ago, but better late than never.

This tool is primarily intended for my projects, so it may not be exactly what you're looking for – it focuses on a single, specific task.
You might prefer to start with more flexible tools like image, ImageMagick, or ffmpeg, which have more customisation to fit a wider variety of use cases.

If you do want to check out my tool, the instructions and source code are all on GitHub: <https://github.com/alexwlchan/create_thumbnail>

[three]: https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)
