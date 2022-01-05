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

I recently rewrote the code that generates these shelves to use Rust, as a way to learn how to do images in Rust.
In this post, I'm going to explain how it works.

You may not want to generate these exact images, but the ability to generate graphics like this has been useful in lots of projects – consider it a primer in creating simple images.

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

We'll choose colours for the individual books later.

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
        // A rectangle whose upper-left corner is at (20, 10), which is
        // 40 pixels wide and 30 pixels tall.
        //
        // The origin is the top left-hand corner, and coordinates
        // increase as you move right and down.
        Rect::at(20, 10).of_size(40, 30),

        // (0, 255, 0) = #00ff00 = green
        // The final '255' is the alpha value = fully opaque
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



## Choosing the rectangle sizes

Now I can draw a single rectangle, I want to draw lots of rectangles.
Each of these will start from the top edge, have a random width and height, and they'll keep going until they fill the entire image.

Let's start by sketching out an API for generating rectangles:

```rust
use std::ops::Range;

struct RectangleOptions {
    width: Range<u32>,
    height: Range<u32>,
    total_width: u32,
}

fn generate_rectangles(options: RectangleOptions) -> Vec<Rect> {
    ...
}

let rectangles = generate_rectangles(
    RectangleOptions {
        width: (5..30),
        height: (60..90),
        total_width: 500,
    }
);
```

I've got a function `generate_rectangles()` that creates a list of rectangles for us to draw.
We pass it the bounds on the width and height of individual rectangles, and the total width we want it to fill.

I'm passing the options as a struct because it's the best way to do named arguments in Rust.
The alternative would be to pass the struct fields directly as parameters to the function, which leads to code like this:

```rust
generate_rectangles((5..30), (60..90), 500)
```

Much less clear!

Originally I had individual struct fields for min/max width and min/max height, but I refactored it to use a [`Range<u32>`].
It expresses the data in a more succinct way, and matches nicely with the API for generating random ranges.

Then we fill in the body of the function.

```rust
use rand::Rng;

fn generate_rectangles(options: RectangleOptions) -> Vec<Rect> {
    let mut result = Vec::new();
    let mut rng = rand::thread_rng();

    let mut x_coord: u32 = 0;

    while x_coord < options.total_width {
        let width = rng.gen_range(options.width.start..options.width.end);
        let height = rng.gen_range(options.height.start..options.height.end);

        let rect = Rect::at(x_coord as i32, 0).of_size(width, height);
        result.push(rect);
        x_coord += width;
    }

    result
}
```

We start with an empty `Vec` and a random number generator.

On each iteration of the `while` loop, we generate a rectangle.
The `gen_range()` function generates a random value for the width/height of the rectangle, within the bounds we've given – these become the new rectangle, which gets added to the result.

The `x_coord` variable tracks how far along we've moved.
We increase it with each new rectangle we add, so all the rectangles are precisely touching but never overlapping.

This is what the output looks like:

```
[
  Rect { left: 0, top: 0, width: 25, height: 66 },
  Rect { left: 25, top: 0, width: 20, height: 85 },
  Rect { left: 45, top: 0, width: 25, height: 68 },
  ...,
]
```

I'm sure there's a clever way to do this with functional programming that doesn't involve two mutable variables, but I like this approach because it's quite simple.
I can see what this is doing, and it'll continue to make sense to me when I've forgotten this code.

[book]: https://rust-random.github.io/book/guide.html
[`Range<u32>`]: https://doc.rust-lang.org/std/ops/struct.Range.html



## Actually drawing the rectangles

We can combine what we've done so far to draw some black rectangles:

```rust
fn main() {
    let width = 500;
    let mut img = RgbaImage::new(width, 100);

    let rectangles = generate_rectangles(
        RectangleOptions {
            width: (4..28),
            height: (60..90),
            total_width: width,
        }
    );

    for r in rectangles {
        draw_filled_rect_mut(&mut img, r, Rgba::from([0, 0, 0, 255]));
    }

    img.save("out.png").unwrap();
}
```

Here are a few examples, which look close to what we want:

<img src="/images/2022/black_shelves1.png">
<img src="/images/2022/black_shelves2.png">
<img src="/images/2022/black_shelves3.png">

Notice that each shelf has a different shape, because we're using a new random number generator each time.
That's fine for certain use cases, but I want the shelf to be the same shape on every page – so the colour changes as you move from page to page, but the shape is always the same.

I can get a consistent shape by replacing the `thread_rng()` with a seeded RNG, like so:

```rust
use rand::prelude::*;
use rand_pcg::Pcg64;

fn generate_rectangles(options: RectangleOptions) -> Vec<Rect> {
    let mut result = Vec::new();
    let mut rng = Pcg64::seed_from_u64(0);

    ...
}
```

This gives me a predictable set of rectangles, which always look the same.
Next: adding colour!



## Choosing the colours

I wanted to choose colours that looked *similar* to the tint colour of the book cover, but not exactly the same.
The "shelves" made of monochrome black rectangles above don't look much like shelves, because you can't see the different between individual "books".

What I wanted to do was take the tint colour, and create lighter/darker shades of it.
That's tricky if you're using the [RGB colour model][rgb], but much easier if you use [HSL (hue, saturation, lightness)][hsl].
If we fix the hue and saturation but vary the lightness, we get different shades.

There's a Rust crate called [`palette`] that seems to have pretty good support for colour calculations.
I've only used a little bit of it so far, but I like what I see, and it let me generate random colours pretty easily.
Here's what that looks like:

```rust
use palette::{FromColor, Hsl, Srgb};
use palette::rgb::Rgb;

fn generate_colour_like(base: Srgb<f32>) -> Srgb<f32> {
    let hsl: Hsl = Hsl::from_color(base);
    let mut rng = rand::thread_rng();

    // The choice of 3/4 and 4/3 is pretty arbitrary -- I chose some
    // numbers that looked okay, and I haven't had reason to think
    // about it further.
    let min_lightness = hsl.lightness * 3.0 / 4.0;
    let max_lightness = hsl.lightness * 4.0 / 3.0;

    let new_lightness = rng.gen_range(min_lightness..max_lightness);
    let new_hsl = Hsl::new(hsl.hue, hsl.saturation, new_lightness);

    Rgb::from_color(new_hsl)
}
```

For example, if I run it repeatedly against <code><span style="color: #d01c11">█</span> #d01c11</code>, the tint colour for this blog, I get this output:

<pre><code><span style="color: #ee3a2f">█</span> Rgb { red: 0.9332129,  green: 0.22605559, blue: 0.18284044, standard: PhantomData }
<span style="color: #da1c12">█</span> Rgb { red: 0.8556082,  green: 0.11517802, blue: 0.06992951, standard: PhantomData }
<span style="color: #d31c11">█</span> Rgb { red: 0.82863057, green: 0.11154642, blue: 0.067724615, standard: PhantomData }
<span style="color: #ba190f">█</span> Rgb { red: 0.7278998,  green: 0.097986504, blue: 0.059491813, standard: PhantomData }
<span style="color: #ec2215">█</span> Rgb { red: 0.9251349,  green: 0.13244599, blue: 0.084003896, standard: PhantomData }</code></pre>

You could get more variation by increasing the min/max lightness you allow -- there's nothing special about the numbers I picked.

[rgb]: https://en.wikipedia.org/wiki/RGB_color_model
[hsl]: https://en.wikipedia.org/wiki/HSL_and_HSV
[`palette`]: https://docs.rs/palette/0.6.0/palette/



## Putting it all together

We can pick a new colour for each rectangle by calling `generate_colour_like()`.
We need to do a bit of work to convert the `palette` colour into an `image` colour, but once that's done we pass it to the `draw()` method:

```rust
fn main() {
    ...

    // #d01c11
    let base_colour = Rgb::new(0.81568627, 0.10980392, 0.06666667);

    for r in rectangles {
        let colour: palette::Srgb<f32> = generate_colour_like(base_colour);

        let colour: image::Rgba<u8> = Rgba::from([
            (colour.red   * 255.0) as u8,
            (colour.green * 255.0) as u8,
            (colour.blue  * 255.0) as u8,
            255
        ]);

        draw_filled_rect_mut(&mut img, r, colour);
    }

    ...
}
```

And here's an example of what it looks like:

<img src="/images/2022/red_shelves.png">

If you want to get the final code from this post, you can download this zipfile, which is the complete Rust project:

{% download /files/2022/rusty-shelves.zip %}

I've been making [simple graphics like this](/all-posts-by-tag/#images) for over five years, and it's as fun now as when I started.
I don't have any great art skills, but I enjoy taking a simple idea (can I arrange coloured rectangles to look like a bookshelf) and turning it into an endless collection of images based on that idea.
Given how much of my computing life is spent on work and productivity and business, it's nice to make things that just look pretty.
