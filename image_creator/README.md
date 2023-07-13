# image_creator

This is a Docker image that creates various sizes/formats of images using ImageMagick.
The Jekyll build process runs this image on-demand, when it needs to create new images.

It exists as a bit of a stopgap until I can run ImageMagick inside my Jekyll image.

## How it works

The Jekyll build process writes a file `.missing_images.json`, which contains a list of all the images that it needs to build.
There's one image per line, and a line looks somethign like:

```json
{
  "out_path": "_site/images/2023/IMG_1234_1x.avif",
  "source_path": "src/_images/2023/IMG_1234.jpg",
  "width": 1024,
  "height": 768
}
```

The `create_images.rb` script reads this file, and uses ImageMagick to create the appropriate images.

## Why can't I run ImageMagick inside my Jekyll image?

I have two conflicting requirements:

*   Jekyll uses Jekyll Sass Converter, which uses [sass-embedded](https://jekyllrb.com/news/2022/12/21/jekyll-sass-converter-3.0-released/) for stylesheets.
    You have to use a glibc flavour of Linux to use sass-embedded, so I use Debian as my base image.

    (See [alexwlchan/alexwlchan.net#594](https://github.com/alexwlchan/alexwlchan.net/issues/594) for more info/links.)

*   I need ImageMagick 7 compiled with AVIF support to create images.

    This isn't available from the apt repositories for Debian 11, and I struggled to get it working using the [IMEI installer script][imei] with AVIF support.
    However, it is available from the Alpine package repos.

It was easier to install ImageMagick 7 inside an Alpine image and run it as a separate container, than keep fiddling with ImageMagick 7 inside a Debian image.

I'd like to collapse ImageMagick back into the main image eventually, but until then this keeps it manageable.

[imei]: https://github.com/SoftCreatR/imei
