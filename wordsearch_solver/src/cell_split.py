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