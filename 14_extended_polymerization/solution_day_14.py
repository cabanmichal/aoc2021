"""https://adventofcode.com/2021/day/14"""

from collections import Counter
from typing import Tuple, Dict, Iterator, Counter as TCounter


class Polymer:
    def __init__(self, template: str, rules: Dict[str, str]) -> None:
        self.polymer = template
        self.rules = rules
        self.counter: TCounter[str] = Counter(self.polymer)

    @staticmethod
    def get_pairs(polymer: str) -> Iterator[str]:
        i = 0
        while i < len(polymer) - 1:
            yield polymer[i] + polymer[i + 1]
            i += 1

    def make_step(self, last_step_pairs: Dict[str, int]) -> Dict[str, int]:
        """Return counts of new polymer pairs."""
        counter: TCounter[str] = Counter()

        for pair, count in last_step_pairs.items():
            element = self.rules[pair]
            self.counter[element] += count

            counter[pair[0] + element] += count
            counter[element + pair[1]] += count

        return counter

    def make_n_steps(self, max_step: int) -> None:
        counter = dict(Counter(self.get_pairs(self.polymer)))
        for _ in range(max_step):
            counter = self.make_step(counter)

    def most_common_least_common_diff(self) -> int:
        counts = self.counter.most_common()
        return counts[0][1] - counts[-1][1]


def parse_input(file: str = "input.txt") -> Tuple[str, Dict[str, str]]:
    rules: Dict[str, str] = {}

    with open(file, "r", encoding="utf-8") as fin:
        template = fin.readline().strip()
        for line in fin:
            line = line.strip()
            if not line:
                continue

            key, value, *_ = line.split(" -> ")
            rules[key] = value

    return template, rules


if __name__ == "__main__":
    template, rules = parse_input("input.txt")
    for idx, steps in enumerate([10, 40]):
        polymer = Polymer(template, rules)
        polymer.make_n_steps(steps)
        solution = polymer.most_common_least_common_diff()

        print(f"Solution {idx + 1}: {solution:13}")  # 2587, 3318837563123
