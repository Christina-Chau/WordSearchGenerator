import random
import string

from src.Board import Board

class Game:
    def __init__(self, word_bank, size):
        self.word_bank = word_bank
        self.board = Board(size).board
        self.size = size

    def can_place(self, positions, word):
        for i, (r, c) in enumerate(positions):
            if self.board[r][c] != '-' and self.board[r][c] != word[i]:
                return False
        return True

    def place_word(self, word):
        word = "".join(word.split())
        attempts = 0
        max_attempts = 100

        best_option = None
        best_overlap = -1

        while attempts < max_attempts:
            attempts += 1
            orientation = random.randint(0, 3)

            reverse = random.choice([True, False])
            placed_word = word[::-1] if reverse else word

            if orientation == 0:  # Horizontal
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - len(word))
                positions = [(row, col + i) for i in range(len(word))]

            elif orientation == 1:  # Vertical
                row = random.randint(0, self.size - len(word))
                col = random.randint(0, self.size - 1)
                positions = [(row + i, col) for i in range(len(word))]

            elif orientation == 2:  # Diagonal ↘
                row = random.randint(0, self.size - len(word))
                col = random.randint(0, self.size - len(word))
                positions = [(row + i, col + i) for i in range(len(word))]

            else:  # Diagonal ↗
                row = random.randint(len(word) - 1, self.size - 1)
                col = random.randint(0, self.size - len(word))
                positions = [(row - i, col + i) for i in range(len(word))]

            if self.can_place(positions, placed_word):
                overlap = sum(
                    1 for i, (r, c) in enumerate(positions)
                    if self.board[r][c] == placed_word[i]
                )

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_option = (positions, placed_word)

        if best_option:
            positions, placed_word = best_option
            for i, (r, c) in enumerate(positions):
                self.board[r][c] = placed_word[i]
            return True

        return False

    def fill_empty(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '-':
                    self.board[r][c] = random.choice(string.ascii_uppercase)

    def create_board(self, words):
        placed_words = []

        for word in words:
            normalized_word = word.upper()
            if self.place_word(normalized_word):
                placed_words.append(normalized_word)
            else:
                print(f"Warning: Could not place word '{word}'")

        self.word_bank = placed_words
        self.fill_empty()
        return self.board, placed_words