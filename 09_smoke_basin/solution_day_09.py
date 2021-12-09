"""https://adventofcode.com/2021/day/9"""

import math
from collections import deque
from typing import List, Tuple, Set, Optional

TPoint = Tuple[int, int]


class HeightMap:
    MAX_HEIGHT = 9

    def __init__(self, heights: List[List[int]]) -> None:
        self.heights = heights
        self.width = len(self.heights[0])
        self.height = len(self.heights)
        self.lows: Optional[List[TPoint]] = None

    def adjacent_points(self, coord_x: int, coord_y: int) -> List[TPoint]:
        points = []
        for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            adj_x = coord_x + dx
            adj_y = coord_y + dy

            if 0 <= adj_x < self.width and 0 <= adj_y < self.height:
                points.append((adj_x, adj_y))

        return points

    def low_points(self) -> List[TPoint]:
        if self.lows is not None:
            return self.lows.copy()

        self.lows = []
        for coord_y in range(self.height):
            for coord_x in range(self.width):
                if self.is_low_point(coord_x, coord_y):
                    self.lows.append((coord_x, coord_y))

        return self.low_points()

    def get_basin(self, point: TPoint) -> List[TPoint]:
        seen: Set[TPoint] = set()
        to_visit = deque([point])
        while to_visit:
            current = to_visit.popleft()
            seen.add(current)
            for adjacent in self.adjacent_points(*current):
                if (
                    self.point_height(*adjacent) < HeightMap.MAX_HEIGHT
                    and adjacent not in seen
                ):
                    to_visit.append(adjacent)
                    seen.add(adjacent)

        return list(seen)

    def is_low_point(self, coord_x: int, coord_y: int) -> bool:
        point_height = self.point_height(coord_x, coord_y)
        adjacent_points = self.adjacent_points(coord_x, coord_y)
        adjacent_heights = (self.point_height(*point) for point in adjacent_points)
        return point_height < min(adjacent_heights)

    def point_height(self, coord_x: int, coord_y: int) -> int:
        return self.heights[coord_y][coord_x]

    def low_point_heights(self) -> List[int]:
        heights = []
        for point in self.low_points():
            heights.append(self.point_height(*point))

        return heights

    def total_risk_level(self) -> int:
        """Answer part 1."""
        return sum(point + 1 for point in self.low_point_heights())

    def largest_basins_product(self) -> int:
        """Answer part 2."""
        basin_sizes = []
        for low_point in self.low_points():
            basin = self.get_basin(low_point)
            basin_sizes.append(len(basin))

        return math.prod(sorted(basin_sizes, reverse=True)[:3])


def parse_input(file: str = "input.txt") -> List[List[int]]:
    heightmap = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            heightmap.append([int(height) for height in line])

    return heightmap


if __name__ == "__main__":
    floor = parse_input("input.txt")
    height_map = HeightMap(floor)
    for idx, solution in enumerate(
        [height_map.total_risk_level(), height_map.largest_basins_product()]
    ):
        print(f"Solution {idx + 1}: {solution:7}")  # 516, 1023660
