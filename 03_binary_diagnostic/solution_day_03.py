"""https://adventofcode.com/2021/day/3"""

from typing import Callable, List

TCountFunc = Callable[[int], str]


class BitCounter:
    def __init__(self, width: int) -> None:
        self.counter = [0] * width

    def add_number(self, number: str) -> None:
        for idx, value in enumerate(number):
            if value == "0":
                self.counter[idx] -= 1
            elif value == "1":
                self.counter[idx] += 1
            else:
                raise ValueError(f"Incorrect format: {number}")

    def add_numbers(self, numbers: List[str]) -> None:
        for number in numbers:
            self.add_number(number)

    def _process_counts(self, func: TCountFunc) -> str:
        """Provide value for count at each index."""
        values = [func(count) for count in self.counter]
        return "".join(values)

    def most_common(self, on_equal: str = "1") -> str:
        return self._process_counts(
            lambda c: "0" if c < 0 else "1" if c > 0 else on_equal
        )

    def least_common(self, on_equal: str = "0") -> str:
        return self._process_counts(
            lambda c: "1" if c < 0 else "0" if c > 0 else on_equal
        )


class ReportAnalyzer:
    def __init__(self, lines: List[str]) -> None:
        if not lines:
            raise ValueError("No lines to analyze")
        self.lines = lines
        self.width = len(lines[0])
        self.counter = BitCounter(self.width)
        self._counted = False

    def _count(self) -> None:
        self.counter.add_numbers(self.lines)
        self._counted = True

    def _get_rating(self, type_: str) -> int:
        if not self._counted:
            self._count()

        lines = self.lines
        index = 0
        while index < self.width and len(lines) > 1:
            counter = BitCounter(self.width)
            counter.add_numbers(lines)

            if type_ == "oxy_gen":
                bit = counter.most_common()[index]
            elif type_ == "co2_scrubber":
                bit = counter.least_common()[index]
            else:
                raise ValueError(f"Unknown rating type: {type_}")

            lines = [line for line in lines if line[index] == bit]
            index += 1

        return int(lines[0], 2)

    def gama_rate(self) -> int:
        if not self._counted:
            self._count()

        return int(self.counter.most_common(), 2)

    def epsilon_rate(self) -> int:
        if not self._counted:
            self._count()

        return int(self.counter.least_common(), 2)

    def power_consumption(self) -> int:
        return self.gama_rate() * self.epsilon_rate()

    def oxy_gen_rating(self) -> int:
        return self._get_rating("oxy_gen")

    def co2_scrubber_rating(self) -> int:
        return self._get_rating("co2_scrubber")

    def life_support_rating(self) -> int:
        return self.oxy_gen_rating() * self.co2_scrubber_rating()


def get_lines(file: str = "input_example.txt") -> List[str]:
    lines = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                lines.append(line)

    return lines


if __name__ == "__main__":
    log_lines = get_lines("input.txt")
    analyzer = ReportAnalyzer(log_lines)
    for idx, solution in enumerate(
        [analyzer.power_consumption(), analyzer.life_support_rating()]
    ):
        print(f"Solution {idx + 1}: {solution}")  # 4138664, 4273224
