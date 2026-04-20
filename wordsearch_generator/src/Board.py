class Board:
    def __init__(self, size = 10):
        self.board = [['-' for _ in range(size)] for _ in range(size)]
        self.size = size

    def print_board(self):
        for row in self.board:
            print(' '.join(row))