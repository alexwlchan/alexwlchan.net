from PIL import Image


def get_crops(im, *, columns, rows):
    column_width = im.width // columns
    row_height = im.height // rows

    for r in range(rows):
        for c in range(columns):
            x = c * column_width
            y = r * row_height
            yield (x, y, x + column_width, y + row_height)


if __name__ == "__main__":
    im = Image.open("artichoke.jpg")

    individual_scans = [im.crop(c) for c in get_crops(im, columns=7, rows=4)]

    individual_scans[0].save(
        "artichoke.gif", save_all=True, append_images=individual_scans[1:]
    )
