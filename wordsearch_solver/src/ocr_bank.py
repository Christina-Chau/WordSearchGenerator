"""
ocr_bank.py

Purpose:
    Read the word bank section of the puzzle page and convert it into a clean
    list of target words.

Responsibilities:
    - Crop the word-bank region from the page
    - Run OCR on the cropped region
    - Normalize OCR text into a usable word list
    - Clean punctuation, whitespace, and casing issues

Why this file exists:
    The puzzle cannot be solved unless we know which words to search for in the
    letter grid. This module extracts that list from the PDF/image.
"""