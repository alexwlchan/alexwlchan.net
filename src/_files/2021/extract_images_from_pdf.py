#!/usr/bin/env python3
"""
This script extracts the images from a PDF file.

Requires:

    pip3 install PyMuPDF Pillow

From https://alexwlchan.net/2021/10/redacting-pdfs/
Based on https://www.thepythoncode.com/code/extract-pdf-images-in-python

"""

import io
import os
import sys

import fitz  # PyMuPDF
from PIL import Image


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <PATH>")

    out_dir = os.path.join("pdf-images", os.path.basename(path))
    os.makedirs(out_dir, exist_ok=True)

    with fitz.open(path) as pdf_file:
        for page_number, page in enumerate(pdf_file, start=1):
            for image_number, image in enumerate(page.getImageList(), start=1):
                # Get the XREF of the image
                xref = image[0]

                # Extract the image bytes
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image["image"]

                # Get the image extension
                image_ext = base_image["ext"]

                # Load it as a Pillow image
                image = Image.open(io.BytesIO(image_bytes))

                # Save it to a file
                out_path = os.path.join(
                    out_dir, f"page{page_number}_{image_number}.{image_ext}"
                )
                image.save(out_path)
                print(out_path)
