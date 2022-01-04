---
layout: post
title: Creating coloured bookshelf graphics in Rust
summary:
tags: rust images
---

In my [last post], I mentioned I have a mini-site where I track the books I've been reading ([books.alexwlchan.net]).
It's mostly meant for my personal use, which is why I don't talk about it much – but today I do want to talk about one of its design elements.

At the top of each page is a header that's meant to look like a gravity-defying bookshelf.
It's made up of coloured rectangles, which look like the spines of books (to my eye, at least):

<figure class="wide_img">
  <img src="/images/2022/shelves.png">
</figure>

Every page on the site has a different-coloured shelf, to match the cover of the book on that page.
For example, these shelves come from books with [a red cover][red], [a yellow cover][yellow], and [a blue cover][blue].

I recently rewrote the code that generates these shelves to use Rust, as a way to learn about images in Rust.
In this post, I'm going to explain how it works.
You may not want to generate these exact images, but the ability to generate simple graphics like this has been useful in lots of projects.

[last post]: /2021/12/2021-in-reading/
[books.alexwlchan.net]: https://books.alexwlchan.net/
[red]: https://books.alexwlchan.net/reviews/trains
[yellow]: https://books.alexwlchan.net/reviews/your-computer-is-on-fire/
[blue]: https://books.alexwlchan.net/reviews/the-power-of-the-a4s



## Choosing the colour of the shelves

Given the cover of a book, how do I decide what colour I should use for the shelves?

This is a problem I've solved before: I use my [dominant_colours tool][dominant_colours] to extract the main colours from the book cover, and I choose the one that I think will look best.
If you're curious how that works, check out [my explainer post][explainer] about *k*-means colouring.

This gives us an RGB colour, like <code><span style="color: #917546">█</span> #917546</code>.

[dominant_colours]: https://github.com/alexwlchan/dominant_colours
[explainer]: /2019/08/finding-tint-colours-with-k-means/



## Creating an empty image

To work with images in Rust, we need to use the [`image` crate].
We add that to our `Cargo.toml`.

Within the `image` crate, an in-memory image is stored in an [`ImageBuffer`].
This struct holds the width, the height, and all the pixels.
Different instances of `ImageBuffer` can hold different types of pixels, like RGB, RGBA, or grayscale.
It's parameterised by pixel type.

We create a new `ImageBuffer` by passing the width and the height.
For example, to create an image which is 200 pixels wide and 100 pixels tall:

```rust
use image::{ImageBuffer, Rgba};

fn main() {
    let img: ImageBuffer<Rgba<u8>, Vec<u8>> = ImageBuffer::new(200, 100);

    img.save("out.png").unwrap();
}
```

We have to provide the type hint to tell the compiler that this instance of `ImageBuffer` should have RGBA pixels.
(I want RGBA because I want anything not part of the bookshelf to be transparent.)

The crate includes some aliases for commonly used pixel types, so we can simplify this slightly:

```rust
use image::RgbaImage;

fn main() {
    let img = RgbaImage::new(200, 100);

    img.save("out.png").unwrap();
}
```

But the image it creates isn't very interesting!

[`image` crate]: https://docs.rs/image/0.23.14/image/index.html
[`ImageBuffer`]: https://docs.rs/image/0.23.14/image/struct.ImageBuffer.html



## Drawing some simple shapes

To draw shapes on the image, I turned to the [`imageproc` crate].
This builds on the `image` crate to add all sorts of helpful functions, and of particular interest here is the [`drawing` module].

For example, let's draw a green rectangle using [`draw_filled_rect`].
We pass the image we're modifying, the rectangle we want to draw, and the colour.
The function returns the new image.

```rust
use image::{RgbaImage, Rgba};
use imageproc::drawing::draw_filled_rect;
use imageproc::rect::Rect;

fn main() {
    let img = RgbaImage::new(200, 100);

    let new_img = draw_filled_rect(
        &img,
        Rect::at(20, 10).of_size(40, 30),
        Rgba::from([0, 255, 0, 255])
    );

    new_img.save("out.png").unwrap();
}
```

Here's what the result looks like:

<img src="/images/2022/green_rectangle.png" style="border: 0.25px solid black;">

You can also modify the image in-place by making the image mutable, and using `draw_filled_rect_mut`:

```rust
use image::{RgbaImage, Rgba};
use imageproc::drawing::draw_filled_rect_mut;
use imageproc::rect::Rect;

fn main() {
    let mut img = RgbaImage::new(200, 100);

    draw_filled_rect_mut(
        &mut img,
        Rect::at(20, 10).of_size(40, 30),
        Rgba::from([0, 255, 0, 255])
    );

    img.save("out.png").unwrap();
}
```

I couldn't find anything in the imageproc documentation to explain when you should prefer one approach over the other.
This means the in-place version is more efficient, but you lose the previous version of the image.
For the rest of this post I'm going to use the in-place version, because I'm building up a single image – but it's a distinction to be aware of.

Here's one more example, to draw multiple shapes on a canvas:

```rust
use image::{RgbaImage, Rgba};
use imageproc::drawing::{
    draw_filled_circle_mut,
    draw_filled_rect_mut,
    draw_polygon_mut,
};
use imageproc::point::Point;
use imageproc::rect::Rect;

fn main() {
    let mut img = RgbaImage::new(200, 100);

    draw_filled_rect_mut(
        &mut img,
        Rect::at(20, 10).of_size(40, 30),
        Rgba::from([0, 255, 0, 255])
    );

    draw_filled_circle_mut(
        &mut img,
        (60, 70),
        15,
        Rgba::from([0, 255, 255, 255])
    );

    draw_polygon_mut(
        &mut img,
        &[Point::new(100, 50), Point::new(100, 100), Point::new(120, 50)],
        Rgba::from([255, 0, 255, 255])
    );

    img.save("out.png").unwrap();
}
```

Without [looking at the result](/images/2022/multiple_shapes.png), can you guess what this looks like?

[copy]: https://github.com/image-rs/imageproc/blob/9c2823b3505f6c8f99d85bfbe233bb231d30f696/src/drawing/rect.rs#L9-L18
[`imageproc` crate]: https://docs.rs/imageproc/0.22.0/imageproc/index.html
[`drawing` module]: https://docs.rs/imageproc/0.22.0/imageproc/drawing/index.html
[`draw_filled_rect`]: https://docs.rs/imageproc/0.22.0/imageproc/drawing/fn.draw_filled_rect.html
