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
    depths = get_input("input.txt")
    for idx, window in enumerate([1, 3]):
        solution = count_increases(depths, window)
        print(f"Solution {idx+1}: {solution}")  # 1548, 1589
