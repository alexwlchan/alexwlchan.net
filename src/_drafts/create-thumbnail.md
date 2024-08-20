---
layout: post
title: "create_thumbnail: create smaller versions of images"
summary:
tags:
  - rust
  - my-tools
  - images
colors:
  css_light: "#1c8034"
  css_dark:  "#94b960"
---
I’ve made a new command-line tool: [create_thumbnail], which creates thumbnails of images.

You tell it your original image, the directory where you're storing thumbnails, and the max width/height of the thumbnail you want to create.
Then it prints the path to the newly-created thumbnail.
Here are two examples:

```console
$ create_thumbnail cat.jpg --out-dir=thumbnails --width=150
./thumbnails/cat.jpg

$ create_thumbnail dog.png --out-dir=thumbnails --height=200
./thumbnails/dog.png
```

It supports JPEG, PNG, TIFF, WEBP, and both static and animated GIFs.
Thumbnails match the format of the original image, except for animated GIFs, which become MP4 movies.

## How does it work?

The heavy lifting is done by the [image crate] and [ffmpeg].

Here's how you can use the image crate to resize an image in Rust:

```rust
let image_path = "pineapple.jpg";
let thumbnail_path = "thumbnail.jpg";

let (width, height) = (306, 204);

image::open(image_path)?
    .resize(width, height, image::imageops::FilterType::Lanczos3)
    .save(thumbnail_path)?;
```

The documentation for the `resize()` method has [some good examples][resize] of the different filter options -- how they affect the quality of the image and the time taken to create it.
I'm using Lanczos with window 3 because it creates the best looking image (to my eyes at least), and I'm not particularly performance constrained.

Here's how you can use ffmpeg to [create an MP4 video of an animated GIF](/til/2024/convert-an-animated-gif-to-mp4/):

```shell
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
```

My tool is a wrapper around these two snippets.
It picks the correct dimensions for the final thumbnail based on the dimensions of the original image and the max width/height, then runs these two snippets to create the thumbnail.

(This turns out to be not completely trivial: something in this ffmpeg command requires that the width/height be even numbers.
If you try to create a file with an odd width/height, the command fails.
This is something I have rediscovered multiple times, and now it's encoded in this tool.)

My tool isn't especially flexible, but it doesn't need to be -- I have a simple use case.
Max width/height is enough for me.

[create_thumbnail]: https://github.com/alexwlchan/create_thumbnail
[image crate]: https://crates.io/crates/image
[ffmpeg]: https://www.ffmpeg.org/
[resize]: https://docs.rs/image/0.25.2/image/imageops/enum.FilterType.html#examples

## Why did I make this?

I've written some version of a thumbnailer in at least a dozen projects.

In each of those projects, the code is of questionable quality.
The thumbnailer was always a sub-feature, so I wrote something that was good enough for that project -- but now I have a bunch of variants, each with a different set of features and bugs.

If I was following the [rule of three], I'd have pulled this out as a standalone component a long time ago.
I'm pretty good at following that rule within a single project, but not across projects.

By pulling my thumbnailer out into a standalone tool, I get a single version of this code that I can use in all my other projects.
And because this code just does thumbnailing, I gave it more attention and care -- this is better code than I ever wrote as a sub-component of another project, because this is just a thumbnailer.
By narrowing my focus to a small amount of code, I spent more time with that code and I made it better.

[rule of three]: https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)
