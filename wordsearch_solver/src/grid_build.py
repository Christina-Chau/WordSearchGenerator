"""
grid_build.py

Purpose:
    Reconstructs a 2D word search board from a folder of cropped cell images
    by applying OCR to each cell and assembling the results into a matrix.

Responsibilities:
    - Load individual cell images from a structured directory (cell_r_c.png)
    - Apply OCR to each cell image to extract a single letter
    - Clean and normalize OCR output (uppercase, fallback handling)
    - Assemble letters into a 2D grid (list of lists)
    - Provide a usable board representation for the solver module

Why this file exists:
    This file acts as the bridge between computer vision preprocessing
    (grid cropping and cell splitting) and the solving algorithm.

    It isolates the logic of reconstructing structured data (a board)
    from unstructured image inputs, allowing:
    - easier debugging of OCR errors
    - modular replacement of OCR (e.g., CNN later)
    - clean separation between perception (vision) and reasoning (solver)
"""

from pathlib import Path
from src.ocr_letters import recognize_letter


def build_board_from_folder(folder_path, grid_size):
    folder = Path(folder_path)

    board = []

    for r in range(grid_size):
        row = []

        for c in range(grid_size):
            cell_path = folder / f"cell_{r}_{c}.png"

            letter = recognize_letter(cell_path)
            row.append(letter)

        board.append(row)

    return board