"""
solver.py

Purpose:
    Solve the word search by locating each target word in the reconstructed
    letter grid.

Responsibilities:
    - Accept a 2D letter grid and a list of words
    - Search horizontally, vertically, and diagonally
    - Support forward and reverse matches
    - Return coordinates for each found word

Why this file exists:
    Once the grid letters and word bank are known, solving the puzzle is best
    handled with deterministic search logic rather than machine learning.
"""