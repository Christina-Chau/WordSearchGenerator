import os
import sys
import json
import shutil

from src.Game import Game
from src.WordBank import WordBank
from fpdf import FPDF, XPos, YPos
from pathlib import Path

RAW_PDF_DIR = Path("../wordsearch_solver/src/data/raw_pdfs")
METADATA_DIR = Path("../wordsearch_solver/src/data/pdf_metadata")

def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt)
        if choice == "q":
            sys.exit(0)
        if choice.lower() in valid_options:
            return choice
        print("Invalid input, try again")

def validate_filename(filename):
    filename = filename.strip()
    if not filename.endswith(".pdf"):
        filename = filename + ".pdf"
    return filename

def save_game_to_file(game, sub_category, bank, filename):
    filename = validate_filename(filename)

    bank.sort(key=str.casefold)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Word Search Game", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, f"Category: {sub_category}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, "Words to Find:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    col_count = 3
    col_width = pdf.epw / col_count
    row_height = 8

    for row_start in range(0, len(bank), col_count):
        pdf.set_x(pdf.l_margin)
        for word in bank[row_start:row_start + col_count]:
            pdf.cell(col_width, row_height, word, border=0)
        pdf.ln(row_height)
    pdf.ln(6)

    grid_size = len(game.board)
    max_cell_size = 10
    max_grid_width = pdf.epw
    max_grid_height = pdf.h - pdf.b_margin - pdf.get_y()
    cell_size = min(max_cell_size, min(max_grid_width, max_grid_height) / grid_size)

    if cell_size < 4:
        pdf.add_page()
        max_grid_height = pdf.h - pdf.t_margin - pdf.b_margin
        cell_size = min(max_cell_size, min(max_grid_width, max_grid_height) / grid_size)

    grid_font_size = min(12, max(5, cell_size * 1.8))
    pdf.set_font("Courier", "", grid_font_size)

    grid_width = cell_size * grid_size
    start_x = pdf.l_margin + (pdf.epw - grid_width) / 2
    pdf.set_x(start_x)

    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.1)

    grid_start_y = pdf.get_y()

    for row in game.board:
        pdf.set_x(start_x)
        for item in row:
            pdf.cell(cell_size, cell_size, str(item), border=1, align="C")
        pdf.ln(cell_size)

    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)

    wordbank_filepath = os.path.join("../WordBanks", filename)
    pdf.output(wordbank_filepath)

    solver_pdf_path = RAW_PDF_DIR / filename
    shutil.copy(wordbank_filepath, solver_pdf_path)

    metadata = {
        "grid_size": grid_size,
        "cell_size_mm": cell_size,
        "start_x_mm": start_x,
        "start_y_mm": grid_start_y,
        "solution_grid": game.board,
        "word_bank": bank
    }

    meta_path = METADATA_DIR / f"{Path(filename).stem}_metadata.json"

    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved PDF to {wordbank_filepath}")
    print(f"Copied PDF to {solver_pdf_path}")
    print(f"Saved metadata to {meta_path}")

def get_word_bank(category, bank):
    subs = bank.get_subcategories(category)

    if len(subs) == 0:
        print("No subcategories exist for this category yet")
        sys.exit(0)

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

    return bank.get_words(category, selected_sub)

def get_and_validate_word_bank(bank):
    words = input("Enter a list of words separated by commas: ").split(",")
    return bank.validate_words(words)

def save_to_word_bank(words, bank):
    save = get_valid_input("Do you want to save your list of words for the future? [Y/N]", ["y", "n"])
    if save.lower() == "y":
        save_name = input("Enter category name for your list of words: ")
        bank.save_to_word_bank(words, save_name)
    else:
        return

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

    word_bank = WordBank(size=size)

    category_map = word_bank.get_categories()

    NEW_OPTION = "N"

    options = ", ".join(
        f"{name}[{idx}]" for idx, name in category_map.items()
    )
    options += f", Create new word bank[{NEW_OPTION}]"

    categoryChosen = get_valid_input(
        f"Choose category ({options}): ",
        list(map(str, category_map.keys())) + ['n']
    )

    words_for_game = []
    cat = ''
    if categoryChosen == 'n' or categoryChosen == 'N':
        custom_map = {
            "1": "list",
            "2": "prompt",
            "q" : "quit"
        }
        # TODO: If there are custom inputs saved then display the custom ones as well
        customChosen = get_valid_input(
            "Choose whether you want to enter a custom list of words (at most 30 words)[1] or a custom prompt[2]: ",
            custom_map.keys()
        )
        if customChosen == '1':
            words_for_game = get_and_validate_word_bank(word_bank)
            save_to_word_bank(words_for_game, word_bank)
        else:
            prompt = input("Enter a category you would like to generate words for: ")
            words_for_game = word_bank.generate_words(prompt, size)
            if words_for_game is None:
                print("Invalid category, goodbye")
                sys.exit(0)
            cat = prompt
            save_to_word_bank(words_for_game, word_bank)
    else:
        cat = category_map[int(categoryChosen)]
        words_for_game = get_word_bank(cat, word_bank)

    print("\nList of words for game: ")
    print(words_for_game)
    print("\n Generating game")

    game = Game(words_for_game, size)
    board, words_for_game = game.create_board(words_for_game)
    print("\nGame created")
    print(board)

    save_result = get_valid_input("Do you want to save the game to a file? (Y/N)", ["y", "n"])
    if save_result == "Y" or save_result == "y":
        file_name = input("Enter file name to save: ")
        save_game_to_file(game, cat, words_for_game, file_name)
        print("\nGame saved")
    else:
        print("\nThanks for playing")
