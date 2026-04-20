# Word Search
Built in Python 3.14, this is a custom word search program.

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

## To Run the Program
Create a virtual environment
```bash
source <venv>/bin/activate
pip3 install -r requirements.pip
python main.py #to run the game
```

## To Utilize the Custom Prompt Generator
This program has the option to generate a list of words with a custom prompt entered in using openAI. The dependency is listed in the requirements.pip file.
Create a .env folder and add
```bash
OPENAI_API_KEY=<insert key here>
```
Run ``source .env`` to import the key