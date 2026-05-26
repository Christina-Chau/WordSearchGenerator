"""
grid_crop.py

Purpose:
    Extract the puzzle grid region from a rendered puzzle image.

Responsibilities:
    - Load a rendered page image
    - Crop out the letter grid area
    - Optionally deskew, threshold, or clean the cropped region

Why this file exists:
    The solver needs a clean image containing only the puzzle grid before
    splitting it into individual cells for letter recognition.
"""

from PIL import Image
from pathlib import Path

import json

from src.layout import mm_to_pixels


def crop_grid(image_path, metadata_path, zoom=3):
    img = Image.open(image_path)

    with open(metadata_path) as f:
        meta = json.load(f)

    start_x = int(mm_to_pixels(meta["start_x_mm"], zoom))
    start_y = int(mm_to_pixels(meta["start_y_mm"], zoom))

    grid_size = meta["grid_size"]

    cell_size_px = mm_to_pixels(
        meta["cell_size_mm"],
        zoom
    )

    total_size = int(cell_size_px * grid_size)

    cropped = img.crop((
        start_x,
        start_y,
        start_x + total_size,
        start_y + total_size
    ))

    return cropped

# Runnable main method for testing
if __name__ == "__main__":
    img_path = Path("data/rendered_images/Bridgerton_page0.png")
    meta_path = Path("data/pdf_metadata/Bridgerton_metadata.json")

    cropped = crop_grid(img_path, meta_path)

    cropped.save("debug_grid.png")