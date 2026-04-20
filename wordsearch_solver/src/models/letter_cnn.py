"""
letter_cnn.py

Purpose:
    Define the neural network used to classify a single puzzle cell image as
    one uppercase letter.

Responsibilities:
    - Build the CNN architecture
    - Expose a model class for training and inference
    - Output probabilities or logits over the alphabet classes

Why this file exists:
    This is the core vision model for reading letters from the puzzle grid one
    cell at a time.
"""