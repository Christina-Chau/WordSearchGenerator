import os
import sys

from src.Game import Game
from src.WordBank import WordBank
from fpdf import FPDF, XPos, YPos

def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt)
        if choice == "q":
            sys.exit(0)
        if choice in valid_options:
            return choice
        print("Invalid input, try again")

def validate_filename(filename):
    filename = filename.strip()
    if not filename.endswith(".pdf"):
        filename = filename + ".pdf"
    return filename

def save_game_to_file(game, sub_category, word_bank, filename):
    filename = validate_filename(filename)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Word Search Game", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Category: {sub_category}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Words to Find:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    words_line = ", ".join(word_bank)
    pdf.multi_cell(0, 8, words_line)
    pdf.ln(5)

    pdf.set_font("Courier", "", 12)
    cell_size = 10
    for row in game.board:
        for item in row:
            pdf.cell(cell_size, cell_size, str(item), border=1, align="C")
        pdf.ln(cell_size)

    os.makedirs("WordBanks", exist_ok=True)
    filepath = os.path.join("WordBanks/", filename)
    pdf.output(filepath)
    print(f"Saved PDF to {filename}")

def get_word_bank(category, word_size):
    wb = WordBank(size=word_size)
    subs = wb.get_subcategories(category)

    print("\nChoose a subcategory:")
    for i, sub in enumerate(subs, start=1):
        print(f"{i}. {sub}")

    valid_sub_choices = [str(i) for i in range(1, len(subs) + 1)]

    sub_choice = get_valid_input(
        "Choose subcategory: ",
        valid_sub_choices
    )

    selected_sub = subs[int(sub_choice) - 1]

    print(f"\nYou selected: {category} → {selected_sub}")

    return wb.get_words(category, selected_sub)

def get_and_validate_word_bank(word_size):
    wb = WordBank(size=word_size)
    words = input("Enter a list of words separated by commas: ").split(",")
    return wb.validate_words(words)

if __name__ == '__main__':
    print("Hello! Welcome to the word search! To quit the process at any time, type 'q'")

    mode_map = {
        "1": 10,
        "2": 20,
        "3": 30,
        "4": "custom"
    }

    modeChosen = get_valid_input(
        "Choose mode (easy[1], medium[2], hard[3], custom[4]): ",
        mode_map.keys()
    )

    size = 0
    if modeChosen == '4':
        while True:
            custom_board_size = int(input("Enter board size between 5 and 50: "))
            if custom_board_size < 5 or custom_board_size > 50:
                print("Invalid input, try again")
            else:
                size = custom_board_size
                break
    else:
        size = mode_map[modeChosen]

    category_map = {
        "1": "seasons",
        "2": "holidays",
        "3": "animals",
        "4": "custom"
    }

    categoryChosen = get_valid_input(
        "Choose category (seasons[1], holidays[2], animals[3], custom[4]): ",
        category_map.keys()
    )

    word_bank = []
    cat = category_map[categoryChosen]
    if categoryChosen == '4':
        custom_map = {
            "1": "list",
            "2": "prompt",
            "q" : "quit"
        }
        customChosen = get_valid_input(
            "Choose whether you want to enter a custom list of words (at most 30 words)[1] or a custom prompt[2]: ",
            custom_map.keys()
        )
        if customChosen == '1':
            word_bank = get_and_validate_word_bank(size)
        else:
            #TODO: Add in prompt generation
            print("Not yet supported")
            sys.exit(0)
    else:
        word_bank = get_word_bank(cat, size)

    print("\nList of words for game: ")
    print(word_bank)
    print("\n Generating game")

    game = Game(word_bank, size)
    create_board = game.create_board(word_bank)
    print("\nGame created")
    print(create_board)

    #TODO: Ask if use wants to save board or not
    file_name = input("Enter file name to save: ")
    save_game_to_file(game, cat, word_bank, file_name)
    print("\nGame saved")