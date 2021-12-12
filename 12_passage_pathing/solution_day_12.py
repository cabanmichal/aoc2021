"""https://adventofcode.com/2021/day/12"""

from collections import defaultdict
from typing import List, Tuple, Set, Dict, Iterator

TCave = str
TCavePair = Tuple[TCave, TCave]
TCaveGraph = Dict[TCave, Set[TCave]]
TPath = List[TCave]

START = "start"
END = "end"


class PathFinder:
    def __init__(self, cave_map: List[TCavePair]) -> None:
        self.path: TPath = []
        self.visited: Dict[TCave, int] = {}
        self.graph = self.make_graph(cave_map)

    @staticmethod
    def make_graph(cave_map: List[TCavePair]) -> TCaveGraph:
        graph: TCaveGraph = defaultdict(set)
        for left, right in cave_map:
            graph[left].add(right)
            graph[right].add(left)

        return graph

    def iter_paths(self, start: TCave = START, end: TCave = END) -> Iterator[TPath]:
        self.visit_cave(start)

        if start == end:
            yield self.path
        else:
            for cave in self.graph[start]:
                if not self.can_be_visited(cave):
                    continue
                yield from self.iter_paths(cave, end)

        self.backtrack(start)

    def visit_cave(self, cave: TCave) -> None:
        self.path.append(cave)
        self.visited.setdefault(cave, 0)
        self.visited[cave] += 1

    def can_be_visited(self, cave: TCave) -> bool:
        visit_count = self.visited.setdefault(cave, 0)
        if (
            self.is_cave_small(cave) or self.is_cave_endpoint(cave)
        ) and visit_count > 0:
            return False
        return True

    def backtrack(self, cave: TCave) -> None:
        self.path.pop()
        self.visited[cave] -= 1

    @staticmethod
    def is_cave_small(cave: TCave) -> bool:
        return cave.lower() == cave and not PathFinder.is_cave_endpoint(cave)

    @staticmethod
    def is_cave_endpoint(cave: TCave) -> bool:
        return cave == START or cave == END


class ReviewedPathFinder(PathFinder):
    def can_be_visited(self, cave: TCave) -> bool:
        visit_count = self.visited.get(cave, 0)

        # any cave not visited yet can be visited
        if not visit_count:
            return True

        # all cases below are for caves already visited at least once
        if self.is_cave_endpoint(cave):
            return False

        if self.is_cave_small(cave):
            small_visited = (c for c in self.path if self.is_cave_small(c))
            small_visit_count = (self.visited[c] for c in small_visited)
            if visit_count > 1 or any(count > 1 for count in small_visit_count):
                return False

        return True


def parse_input(file: str = "input.txt") -> List[TCavePair]:
    lines = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            left, right, *_ = line.split("-")
            lines.append((left, right))

    return lines


if __name__ == "__main__":
    caves = parse_input("input.txt")
    for idx, finder in enumerate([PathFinder, ReviewedPathFinder]):
        path_count = 0
        for _ in finder(caves).iter_paths():
            path_count += 1
        print(f"Solution {idx + 1}: {path_count:5}")  # 3463, 91533
