"""
pdf_render.py

Purpose:
    Convert input word-search PDFs into raster images so they can be processed
    by computer vision and OCR steps.

Responsibilities:
    - Load PDF files from data/raw_pdfs/
    - Render each page to an image
    - Save rendered pages to data/rendered_images/

Why this file exists:
    Most vision pipelines work on images, not PDFs. This module is the bridge
    between the original generated puzzle PDF and the downstream image-based
    processing pipeline.
"""