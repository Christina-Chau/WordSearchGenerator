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
import fitz
from pathlib import Path

RAW_DIR = Path("data/raw_pdfs")
OUT_DIR = Path("data/rendered_images")

OUT_DIR.mkdir(parents=True, exist_ok=True)


def render_pdf(pdf_path, zoom=3):
    doc = fitz.open(pdf_path)

    print(f"Rendering: {pdf_path.name}")

    for page_num, page in enumerate(doc):
        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

        out_path = OUT_DIR / f"{pdf_path.stem}_page{page_num}.png"

        pix.save(out_path)

        print(f"  Saved: {out_path}")

    doc.close()


if __name__ == "__main__":
    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDFs found.")
    else:
        for pdf_path in pdf_files:
            render_pdf(pdf_path)