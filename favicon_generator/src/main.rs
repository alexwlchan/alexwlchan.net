#![deny(warnings)]

use image::{RgbaImage, Rgba};
use imageproc::drawing::{draw_filled_rect_mut, draw_text_mut};
use imageproc::rect::Rect;
use rusttype::{Font, Scale};

fn draw_48px_favicon(colour: Rgba<u8>, font: &Font, out_path: &str) -> () {
    let mut img = RgbaImage::new(48, 48);

    let rect = Rect::at(3, 3).of_size(3, 42);
    draw_filled_rect_mut(&mut img, rect, colour);

    let rect = Rect::at(3, 3).of_size(9, 3);
    draw_filled_rect_mut(&mut img, rect, colour);

    let rect = Rect::at(3, 42).of_size(9, 3);
    draw_filled_rect_mut(&mut img, rect, colour);

    let rect = Rect::at(39, 3).of_size(3, 42);
    draw_filled_rect_mut(&mut img, rect, colour);

    let rect = Rect::at(33, 3).of_size(9, 3);
    draw_filled_rect_mut(&mut img, rect, colour);

    let rect = Rect::at(33, 42).of_size(9, 3);
    draw_filled_rect_mut(&mut img, rect, colour);

    let height = 40 as f32;
    let scale = Scale { x: height * 1.0, y: height };
    draw_text_mut(&mut img, colour, 14, 2, scale, &font, "a");

    img.save(out_path).unwrap();
}

fn main() {
    let red = Rgba::from([208, 28, 17, 255]);

    let font = Vec::from(include_bytes!("../fonts/Georgia.ttf") as &[u8]);
    let font = Font::try_from_bytes(&font).unwrap();

    draw_48px_favicon(red, &font, "out.png");
}
