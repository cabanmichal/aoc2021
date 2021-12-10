"""https://adventofcode.com/2021/day/10"""

import statistics
from dataclasses import dataclass
from enum import Enum
from typing import List

LEFT = "([{<"
RIGHT = ")]}>"
OPENING = set(LEFT)
CLOSING = set(RIGHT)
PAIRS = dict(zip(LEFT, RIGHT))
POINTS_CORRUPTED = dict(zip(RIGHT, [3, 57, 1197, 25137]))
POINTS_INCOMPLETE = dict(zip(RIGHT, [1, 2, 3, 4]))


class LineState(Enum):
    OK = 0
    INCOMPLETE = 1
    CORRUPTED = 2


@dataclass
class LineAnalysisResult:
    state: LineState
    characters: str = ""


def analyze_line(line: str) -> LineAnalysisResult:
    stack: List[str] = []
    for bracket in line:
        if bracket in CLOSING:
            if not stack:
                return LineAnalysisResult(LineState.CORRUPTED, bracket)
            opening = stack.pop()
            if bracket != PAIRS.get(opening):
                return LineAnalysisResult(LineState.CORRUPTED, bracket)
        elif bracket in OPENING:
            stack.append(bracket)
        else:
            return LineAnalysisResult(LineState.CORRUPTED, bracket)

    if stack:
        closing = "".join(PAIRS[b] for b in reversed(stack))
        return LineAnalysisResult(LineState.INCOMPLETE, closing)

    return LineAnalysisResult(LineState.OK)


def score_corrupted_lines(lines: List[str]) -> int:
    score = 0
    for line in lines:
        result = analyze_line(line)
        if result.state == LineState.CORRUPTED:
            score += POINTS_CORRUPTED[result.characters]

    return score


def score_incomplete_lines(lines: List[str]) -> int:
    line_scores = []
    for line in lines:
        line_score = 0
        result = analyze_line(line)
        if result.state != LineState.INCOMPLETE:
            continue
        for c in result.characters:
            line_score *= 5
            line_score += POINTS_INCOMPLETE[c]
        line_scores.append(line_score)

    return int(statistics.median(sorted(line_scores)))


def parse_input(file: str = "input.txt") -> List[str]:
    lines = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            lines.append(line)

    return lines


if __name__ == "__main__":
    lines = parse_input("input.txt")
    for idx, solution in enumerate(
        [score_corrupted_lines(lines), score_incomplete_lines(lines)]
    ):
        print(f"Solution {idx + 1}: {solution:10}")  # 311895, 2904180541
