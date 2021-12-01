"""https://adventofcode.com/2021/day/1"""

from typing import List


def get_input(file: str = "input.txt") -> List[int]:
    lines = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                lines.append(int(line))

    return lines


def count_increases(depths: List[int], window: int = 1) -> int:
    last = sum(depths[:window])
    count = 0
    idx = window
    while idx < len(depths) - window + 1:
        current = sum(depths[idx : idx + window])
        if current > last:
            count += 1
        last = current
        idx += 1

    return count


if __name__ == "__main__":
    solution1 = count_increases(get_input("input.txt"))
    print(f"Solution 1: {solution1}")
    solution2 = count_increases(get_input("input.txt"), window=3)
    print(f"Solution 2: {solution2}")
