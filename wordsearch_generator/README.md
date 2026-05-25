# Word Search
Built in Python 3.14, this is a custom word search program. 
Currently in the works is a CNN that will try to solve a word search.

## Developer Setup

### Prerequisites
- Python 3.14

### Create a virtual environment
```bash
python3 -m venv .venv
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
- Medium 20 x 20 around 20 words
- Hard 30 x 30 around 30 words
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