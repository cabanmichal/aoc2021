"""https://adventofcode.com/2021/day/15"""

import heapq
from typing import Tuple, Dict, List, Set

TPoint = Tuple[int, int]


class Cave:
    def __init__(self, risk_map: List[List[int]]) -> None:
        self.risk_map = risk_map
        self.width = len(risk_map[0])
        self.height = len(risk_map)
        self.start = (0, 0)
        self.goal = (self.width - 1, self.height - 1)
        self.multiplier = 5
        self.risk_wrap = 9

    def child_parent_map(self) -> Dict[TPoint, TPoint]:
        """Get map of nodes to their "parents" that are closest to start.

        Using Dijkstra's algorithm, no optimizations.
        Might be probably solved easier taking into account that we're moving
        diagonally:
        we can solve recursively for row + 1, column + 1 taking minimum of these
        two solutions as a risk...
        """
        start = self.start

        # map of points to the parents that take them fastest to start
        parent_map: Dict[TPoint, TPoint] = {}
        # map of points to their distances from start (float because of "inf")
        distances: Dict[TPoint, float] = {start: 0}
        # heap to keep nodes sorted by their instances from start
        heap: List[Tuple[int, TPoint]] = [(0, start)]
        # keep track of nodes that had been visited
        visited: Set[TPoint] = set()

        heapq.heapify(heap)
        while heap:
            distance, point = heapq.heappop(heap)
            if point in visited:
                continue
            visited.add(point)
            for neighbor in self.get_adjacent(point):
                neighbor_distance = distance + self.get_risk(neighbor)
                if neighbor_distance < distances.get(neighbor, float("inf")):
                    distances[neighbor] = neighbor_distance
                    heapq.heappush(heap, (neighbor_distance, neighbor))
                    parent_map[neighbor] = point

        return parent_map

    def path_to_goal(self) -> List[TPoint]:
        """List of points from start to goal."""
        path: List[TPoint] = []
        parent_map = self.child_parent_map()
        x, y = self.goal
        x = (x + 1) * self.multiplier - 1
        y = (y + 1) * self.multiplier - 1
        current = (x, y)
        while current != self.start:
            path.append(current)
            current = parent_map[current]
        path.append(current)

        return path[::-1]

    def get_adjacent(self, point: TPoint) -> List[TPoint]:
        """Neighbors of given point."""
        points: List[TPoint] = []
        directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        x, y = point
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if (
                0 <= nx < self.width * self.multiplier
                and 0 <= ny < self.height * self.multiplier
            ):
                points.append((nx, ny))

        return points

    def get_lowest_total_risk(self) -> int:
        """Solution to both parts."""
        total = 0
        for point in self.path_to_goal()[1:]:
            total += self.get_risk(point)

        return total

    def get_risk(self, point: TPoint) -> int:
        """Get risk of particular point."""
        x, y = point
        x_plus, x_coord = divmod(x, self.width)
        y_plus, y_coord = divmod(y, self.height)
        risk = self.risk_map[y_coord][x_coord] + x_plus + y_plus
        risk -= self.risk_wrap * ((risk - 1) // self.risk_wrap)

        return risk


def parse_input(file: str = "input.txt") -> List[List[int]]:
    lines = []
    with open(file, "r", encoding="utf-8") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            lines.append([int(n) for n in line])

    return lines


if __name__ == "__main__":
    lines = parse_input("input.txt")
    cave = Cave(lines)
    for idx, multiplier in enumerate([1, 5]):
        cave.multiplier = multiplier
        solution = cave.get_lowest_total_risk()
        print(f"Solution {idx + 1}: {solution:4}")  # 581, 2916
