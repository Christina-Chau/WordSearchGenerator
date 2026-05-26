"""
layout.py

Purpose:
    Define page layout rules and coordinate regions for the puzzle grid and
    word bank.

Responsibilities:
    - Store fixed crop coordinates for known PDF layouts
    - Provide reusable layout configuration values
    - Centralize page geometry assumptions

Why this file exists:
    Since the word-search PDFs are generated in a predictable format, we can
    use fixed or semi-fixed coordinates instead of training a layout detection
    model. This keeps layout logic in one place.
"""

POINTS_PER_MM = 72 / 25.4


def mm_to_pixels(mm, zoom):
    return mm * POINTS_PER_MM * zoom