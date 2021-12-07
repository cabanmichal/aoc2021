"""https://adventofcode.com/2021/day/6"""

from typing import List


def get_fish_count(
    initial_state: List[int],
    days: int,
    first_child_days: int = 9,
    other_child_days: int = 7,
) -> int:
    """Calculate number of fish after given number of days."""
    counter = [0] * first_child_days  # counter for all possible timer states
    for fish in initial_state:
        counter[fish] += 1

    for _ in range(days):
        new_fish = counter[0]
        i = 1
        while i < len(counter):
            counter[i - 1] = counter[i]
            i += 1
        counter[other_child_days - 1] += new_fish
        counter[first_child_days - 1] = new_fish

    return sum(counter)


def parse_input(file: str = "input_example.txt") -> List[int]:
    with open(file, "r", encoding="utf-8") as fh:
        return [int(n) for n in next(fh).strip().split(",")]


if __name__ == "__main__":
    fish = parse_input("input.txt")
    for idx, days in enumerate([80, 256]):
        count = get_fish_count(fish, days)
        print(f"Solution {idx + 1}: {count:13}")  # 393019, 1757714216975
