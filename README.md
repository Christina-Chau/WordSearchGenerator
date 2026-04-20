# Word Search
Built in Python 3.14, this is a custom word search program. 
Currently in the works is a CNN that will try to solve a word search.

## Developer Setup

### Prerequisites
- Python 3.14

### Create a virtual environment
```bash
source <venv>/bin/activate
pip3 install -r requirements.pip
cd wordsearch_generator
python main.py #to run the game
```

## To Utilize the Custom Prompt Generator
This program has the option to generate a list of words with a custom prompt entered in using openAI through OpenRouter. The dependency is listed in the requirements.pip file.
Create a .env folder and add a key from OpenRouter
```bash
OPENROUTER_API_KEY=<insert key here>
```
Run ``source .env`` to import the key. For more information: https://openrouter.ai/openai/gpt-oss-120b:free

## Game Breakdown
Four modes
- Easy 10 x 10 around 10 words
- Medium 20 x 20 around 15 words
- Hard 30 x 30 20 around 20 words
- A custom board size based on user input

Users can feed in a list of words that are length of size of grid maximum. Or choose from preselected list/ enter in a custom list of words.
The word search is then randomly generated. This word search only outputs a 2D array and if the user chooses so, a PDF 
of the search and not meant to be played in program (could be in future iterations).

Categories
- Seasons
  - Fall
  - Spring
  - Summer
  - Winter
- Holidays
  - Valentines
  - Christmas
  - Halloween
  - New Years
  - Thanksgiving
- Animals
  - Sea Animals
  - Land Animals
  - Pets
- Custom (if the user has previously created and wanted to save the list of words)

The existing word bank is saved in json file in WordBanks folder.

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
### Resources
- https://arxiv.org/html/1806.10866v2