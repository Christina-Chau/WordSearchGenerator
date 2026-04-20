"""
infer_letters.py

Purpose:
    Run trained-model inference on cropped puzzle cells and reconstruct the full
    letter grid.

Responsibilities:
    - Load a trained checkpoint
    - Predict the letter in each cropped cell
    - Rebuild the NxN puzzle grid in row/column order
    - Return the reconstructed board for solving

Why this file exists:
    After training, this module applies the model to new puzzles and produces
    the letter grid needed by the solver.
"""