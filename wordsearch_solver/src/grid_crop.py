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