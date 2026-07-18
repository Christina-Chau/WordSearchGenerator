# This file is intentionally empty.
# The game engine is now imported directly from:
#   wordsearch_generator/src/Game.py
#   wordsearch_generator/src/WordBank.py


class Board:
    def __init__(self, size=10):
        self.board = [['-' for _ in range(size)] for _ in range(size)]
        self.size = size


class GameEngine:
    """
    Standalone game engine adapted from wordsearch_generator/src/Game.py.
    Generates a word-search board as a 2D array.
    """

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
        if len(word) > self.size:
            return False

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
                if self.size - len(word) < 0:
                    continue
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - len(word))
                positions = [(row, col + i) for i in range(len(word))]

            elif orientation == 1:  # Vertical
                if self.size - len(word) < 0:
                    continue
                row = random.randint(0, self.size - len(word))
                col = random.randint(0, self.size - 1)
                positions = [(row + i, col) for i in range(len(word))]

            elif orientation == 2:  # Diagonal ↘
                if self.size - len(word) < 0:
                    continue
                row = random.randint(0, self.size - len(word))
                col = random.randint(0, self.size - len(word))
                positions = [(row + i, col + i) for i in range(len(word))]

            else:  # Diagonal ↗
                if len(word) - 1 >= self.size:
                    continue
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
        """Place words and fill remaining cells. Returns (board_2d_array, placed_words)."""
        placed_words = []
        for word in words:
            normalized = word.upper().replace(' ', '')
            if self.place_word(normalized):
                placed_words.append(normalized)
            else:
                print(f"Warning: Could not place '{word}'")

        self.fill_empty()
        return self.get_board_array(), placed_words

    def get_board_array(self):
        """Returns the puzzle as a 2D list of uppercase letters."""
        return [row[:] for row in self.board]
