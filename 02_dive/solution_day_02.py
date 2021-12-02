"""https://adventofcode.com/2021/day/2"""

from dataclasses import dataclass
from typing import List


@dataclass
class Move:
    direction: str
    steps: int


@dataclass
class Position:
    horizontal: int = 0
    vertical: int = 0

    def move(self, where: Move) -> None:
        direction = where.direction
        steps = where.steps
        if direction == "up":
            self.vertical -= steps
        elif direction == "down":
            self.vertical += steps
        elif direction == "forward":
            self.horizontal += steps
        else:
            raise ValueError(f"Unknown direction: {direction}")


@dataclass
class AimedPosition(Position):
    aim: int = 0

    def move(self, where: Move) -> None:
        direction = where.direction
        steps = where.steps
        if direction == "up":
            self.aim -= steps
        elif direction == "down":
            self.aim += steps
        elif direction == "forward":
            self.horizontal += steps
            self.vertical += self.aim * steps
        else:
            raise ValueError(f"Unknown direction: {direction}")


def load_moves(file: str = "input.txt") -> List[Move]:
    moves = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                direction, steps = line.split()
                moves.append(Move(direction, int(steps)))

    return moves


if __name__ == "__main__":
    moves = load_moves("input.txt")
    for idx, position in enumerate([Position(), AimedPosition()]):
        for move in moves:
            position.move(move)
        solution = position.vertical * position.horizontal
        print(f"Solution {idx+1}: {solution:10}")  # 1670340, 1954293920
