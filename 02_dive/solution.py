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
    aim: int = 0

    def move_simple(self, where: Move) -> None:
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

    def move_with_aim(self, where: Move) -> None:
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

    position = Position()
    for move in moves:
        position.move_simple(move)
    solution1 = position.vertical * position.horizontal
    print(f"Solution 1: {solution1}")

    position = Position()
    for move in moves:
        position.move_with_aim(move)
    solution2 = position.vertical * position.horizontal
    print(f"Solution 2: {solution2}")
