"""https://adventofcode.com/2021/day/4"""

from typing import List, Dict, Tuple

TGame = List["Board"]


class Board:
    def __init__(self, board: List[List[int]]) -> None:
        self.board: Dict[int, Tuple[int, int]] = {}
        self.state: List[List[bool]] = []
        self.last_number: int = -1
        self._init(board)

    def _init(self, board: List[List[int]]) -> None:
        for r, row in enumerate(board):
            row_state = []

            for c, num in enumerate(row):
                self.board[num] = (r, c)
                row_state.append(False)

            self.state.append(row_state)

    def is_row_filled(self) -> bool:
        for row in self.state:
            if all(row):
                return True
        return False

    def is_col_filled(self) -> bool:
        for idx in range(len(self.state[0])):
            col_state = [row[idx] for row in self.state]
            if all(col_state):
                return True
        return False

    def is_won(self) -> bool:
        return self.is_row_filled() or self.is_col_filled()

    def add_number(self, num: int) -> None:
        coordinates = self.board.get(num)
        if coordinates is not None:
            row, col = coordinates
            self.state[row][col] = True
        self.last_number = num

    def score(self) -> int:
        total = 0
        for num, (row, col) in self.board.items():
            if not self.state[row][col]:
                total += num

        return total * self.last_number


def parse_input(file: str = "input.txt") -> Tuple[List[int], TGame]:
    boards = []
    with open(file, "r", encoding="utf-8") as fh:
        numbers = [int(n) for n in next(fh).strip().split(",")]

        board = []
        for line in fh:
            row = [int(n) for n in line.strip().split()]
            if row:
                board.append(row)
            if len(board) == 5:
                boards.append(Board(board))
                board = []

    return numbers, boards


def play(numbers: List[int], boards: TGame, order: int) -> int:
    state = [False for _ in boards]
    if order < 0:
        order = len(boards) + order + 1
    won = 0

    for number in numbers:
        for idx, board in enumerate(boards):
            if state[idx]:  # game already won
                continue
            board.add_number(number)
            if not board.is_won():
                continue
            state[idx] = True
            won += 1
            if won == order:
                return board.score()
    return -1


if __name__ == "__main__":
    game_numbers, game_boards = parse_input("input.txt")
    for idx, win_order in enumerate([1, -1]):
        score = play(game_numbers, game_boards, win_order)
        print(f"Solution {idx + 1}: {score}")  # 8580, 9576
