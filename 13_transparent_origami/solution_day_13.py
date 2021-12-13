"""https://adventofcode.com/2021/day/13"""

import re
from typing import List, Tuple, Set, Iterable, Sequence

TPoint = Tuple[int, int]
TInstruction = Tuple[str, int]


def paper_as_str(paper: Iterable[TPoint], dot: str = "###", blank: str = "   ") -> str:
    x_min = float("inf")
    x_max = float("-inf")
    y_min = float("inf")
    y_max = float("-inf")

    for x, y in paper:
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    rows = []
    for y in range(int(y_min), int(y_max) + 1):
        row = []
        for x in range(int(x_min), int(x_max) + 1):
            if (x, y) in paper:
                row.append(dot)
            else:
                row.append(blank)
        rows.append("".join(row))

    return "\n".join(rows)


def fold_x(paper: Iterable[TPoint], coordinate: int) -> Set[TPoint]:
    folded = set()
    for point in paper:
        x, y = point
        if x <= coordinate:
            folded.add(point)
            continue

        new_x = 2 * coordinate - x
        folded.add((new_x, y))

    return folded


def fold_y(paper: Iterable[TPoint], coordinate: int) -> Set[TPoint]:
    folded = set()
    for point in paper:
        x, y = point
        if y <= coordinate:
            folded.add(point)
            continue

        new_y = 2 * coordinate - y
        folded.add((x, new_y))

    return folded


def fold(paper: Iterable[TPoint], instruction: TInstruction) -> Set[TPoint]:
    axis, coord = instruction
    if axis == "x":
        return fold_x(paper, coord)
    if axis == "y":
        return fold_y(paper, coord)
    raise ValueError(f"Wrong axis name: {axis}")


def parse_input(file: str = "input.txt") -> Tuple[List[TPoint], List[TInstruction]]:
    pattern_point = re.compile(r"(\d+),(\d+)")
    pattern_instruction = re.compile(r"fold along ([xy])=(\d+)")
    pts: List[Sequence[str]] = []
    cmd: List[Sequence[str]] = []

    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue

            for container, pattern in zip(
                [pts, cmd], [pattern_point, pattern_instruction]
            ):
                match = pattern.search(line)
                if match is not None:
                    container.append(match.groups())
                    break

    points = [(int(x), int(y)) for x, y, *_ in pts]
    instructions = [(str(ax), int(val)) for ax, val in cmd]

    return points, instructions


if __name__ == "__main__":
    points, instructions = parse_input("input.txt")
    folded = fold(points, instructions[0])
    print(f"Solution 1: {len(folded)}")  # 781

    for instruction in instructions[1:]:
        folded = fold(folded, instruction)
    sol2_file = "output.txt"
    with open(sol2_file, "wt", encoding="utf-8") as fh:
        fh.write(paper_as_str(folded))
    print(f"Solution 2: see: {sol2_file}")  # PERCGJPB
