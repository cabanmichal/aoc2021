"""https://adventofcode.com/2021/day/5"""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Iterator


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Line:
    start: Point
    end: Point

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def iter_points(self) -> Iterator[Point]:
        x_step = 1 if self.start.x <= self.end.x else -1
        y_step = 1 if self.start.y <= self.end.y else -1
        x_coords = range(self.start.x, self.end.x + x_step, x_step)
        y_coords = range(self.start.y, self.end.y + y_step, y_step)

        if self.is_horizontal() or self.is_vertical():
            for x_coord in x_coords:
                for y_coord in y_coords:
                    yield Point(x_coord, y_coord)
        else:
            for x_coord, y_coord in zip(x_coords, y_coords):
                yield Point(x_coord, y_coord)


class OceanFloor:
    def __init__(self) -> None:
        self.vents: Dict[Point, int] = defaultdict(int)

    def add_line(self, line: Line) -> None:
        for point in line.iter_points():
            self.vents[point] += 1

    def iter_overlapping(self, low_limit: int = 2) -> Iterator[Point]:
        for vent, count in self.vents.items():
            if count >= low_limit:
                yield vent


def parse_input(file: str = "input.txt") -> List[Line]:
    pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")
    lines = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            match = pattern.search(line)
            if match is None:
                continue
            coordinates = [int(m) for m in match.groups()]
            start = Point(coordinates[0], coordinates[1])
            end = Point(coordinates[2], coordinates[3])
            lines.append(Line(start, end))

    return lines


def get_vent_count(
    lines: List[Line], low_limit: int = 2, skip_diagonals: bool = True
) -> int:
    floor = OceanFloor()
    for line in lines:
        if skip_diagonals and not (line.is_vertical() or line.is_horizontal()):
            continue
        floor.add_line(line)

    count = 0
    for _ in floor.iter_overlapping(low_limit=low_limit):
        count += 1

    return count


if __name__ == "__main__":
    lines = parse_input("input.txt")
    for idx, solution in enumerate(
        [get_vent_count(lines), get_vent_count(lines, skip_diagonals=False)]
    ):
        print(f"Solution {idx + 1}: {solution}")  # 6710, 20121
