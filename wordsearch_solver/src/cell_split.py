"""
cell_split.py

Purpose:
    Split the cropped puzzle grid into individual cell images, where each cell
    contains a single letter.

Responsibilities:
    - Divide the grid into an N x N set of cells
    - Crop each cell image
    - Save or return the cell images in reading order
    - Preserve row/column position metadata if needed

Why this file exists:
    The letter classifier works on one cell at a time. This module converts the
    full puzzle grid into the smaller units needed for model inference or
    training data generation.
"""

from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "cropped_cells"

def split_cells(grid_img, grid_size):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    width, height = grid_img.size

    cell_w = width / grid_size
    cell_h = height / grid_size

    cells = []

    for r in range(grid_size):
        row = []

        for c in range(grid_size):
            left = int(c * cell_w)
            top = int(r * cell_h)
            right = int((c + 1) * cell_w)
            bottom = int((r + 1) * cell_h)

            cell = grid_img.crop((left, top, right, bottom))

            cell_path = OUTPUT_DIR / f"cell_{r}_{c}.png"
            cell.save(cell_path)

            row.append(cell_path)

        cells.append(row)

    return cells