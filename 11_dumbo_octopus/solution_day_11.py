"""https://adventofcode.com/2021/day/11"""

import copy
from collections import deque
from typing import List, Tuple, Set, Deque

TPoint = Tuple[int, int]


class OctopusGrid:
    def __init__(self, octopuses: List[List[int]]) -> None:
        self.grid = copy.deepcopy(octopuses)
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.grid)

    def find_neighbors(self, octopus: TPoint) -> List[TPoint]:
        x, y = octopus
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))

        return neighbors

    def make_step(self) -> int:
        # increase energy level of all octopuses by 1
        for r in range(self.height):
            for c in range(self.width):
                self.grid[r][c] += 1

        # find octopuses that are about to flash
        flashed: Set[TPoint] = set()
        to_flash: Deque[TPoint] = deque()
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] > 9:
                    to_flash.append((r, c))

        # while there are octopuses to be flashed, flash them
        while to_flash:
            octopus = to_flash.popleft()
            if octopus in flashed:
                continue
            flashed.add(octopus)
            for neighbor in self.find_neighbors(octopus):
                r, c = neighbor
                self.grid[r][c] += 1
                if self.grid[r][c] > 9 and neighbor not in flashed:
                    to_flash.append(neighbor)

        # set energy level of flashed octopuses to 0
        for r, c in flashed:
            self.grid[r][c] = 0

        return len(flashed)

    def make_n_steps(self, number: int) -> int:
        total = 0
        for _ in range(number):
            total += self.make_step()

        return total

    def full_flash(self) -> int:
        steps = 1
        while True:
            flashed = self.make_step()
            if flashed == self.size():
                return steps
            steps += 1

    def size(self) -> int:
        return self.width * self.height


def parse_input(file: str = "input.txt") -> List[List[int]]:
    lines = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            lines.append([int(n) for n in line])

    return lines


if __name__ == "__main__":
    grid = parse_input("input.txt")
    for idx, solution in enumerate(
        [OctopusGrid(grid).make_n_steps(100), OctopusGrid(grid).full_flash()]
    ):
        print(f"Solution {idx + 1}: {solution:4}")  # 1571, 387
