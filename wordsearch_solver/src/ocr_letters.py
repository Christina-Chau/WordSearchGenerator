"""
ocr_letters.py

Purpose:
    Read the letters and categorizing it

Responsibilities:
    - Run OCR on the letters

Why this file exists:
    We need a way to recognize the letters in the grid
"""

import cv2
import pytesseract

def preprocess_image(image_path):
    img = cv2.imread(str(image_path))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh

def recognize_letter(cell_path):
    processed = preprocess_image(cell_path)

    config = r"--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    text = pytesseract.image_to_string(processed, config=config)

    text = text.strip().upper()

    if not text:
        return "?"

    return text[0]