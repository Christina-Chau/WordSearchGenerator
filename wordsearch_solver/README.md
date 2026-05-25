## The CNN Model
### Project Structure
```
wordsearch_solver/
  data/
    raw_pdfs/          # Original generated word-search PDFs used as input
    rendered_images/   # PDF pages converted into images for computer vision processing
    cropped_cells/     # Individual letter-cell image crops used for training/evaluation

  src/
    pdf_render.py      # Converts PDFs into raster images
    layout.py          # Stores layout rules and page-region coordinates
    grid_crop.py       # Extracts the puzzle grid region from the rendered page
    cell_split.py      # Splits the grid into individual letter cells
    ocr_bank.py        # Reads the word bank text from the page using OCR
    solver.py          # Solves the word search by locating words in the letter grid
    annotate.py        # Draws the solved word locations onto an image or PDF

    models/
      letter_cnn.py    # Defines the CNN model for classifying single-letter cell images
      train_letters.py # Trains the CNN on cropped cell images
      infer_letters.py # Runs inference on cropped cells to reconstruct the puzzle grid

  notebooks/
    error_analysis.ipynb  # Used for debugging model mistakes and OCR/grid errors

  outputs/
    solved_images/     # Final solved puzzle images with highlights/annotations
    solved_pdfs/       # Final solved PDFs with highlighted word paths
```

If the sub folders in `data/` are not created, create them. This folder stores the pdfs, images, and cells that are 
created after `pdf_render.py` are called.

### Resources
- https://arxiv.org/html/1806.10866v2