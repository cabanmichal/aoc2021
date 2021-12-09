"""https://adventofcode.com/2021/day/8"""

import itertools
from typing import List, Tuple, Dict, Set

WIRES = "abcdefg"
DIGITS = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}
EASY_DIGITS_LENGTHS = {2: "cf", 3: "acf", 4: "bcdf", 7: "abcdefg"}

TEntry = Tuple[List[str], List[str]]


def wires_to_digits(patterns: List[str]) -> Dict[str, str]:
    """Return mapping of scrambled control wires to "easy digits" (1, 4, 7, 8).

    Keys are sorted by length.
    """
    mapping = {}
    for pattern in sorted(patterns, key=len):
        digit = EASY_DIGITS_LENGTHS.get(len(pattern))
        if digit is None:
            continue
        mapping[pattern] = digit

    return mapping


def wires_to_possible_segments(patterns: List[str]) -> Dict[str, List[str]]:
    """Return mapping of single control wires to possible segments.

    Keys are sorted alphabetically.
    """
    mapping = {}
    mapped_segments: Set[str] = set()
    for wires, digit_segments in wires_to_digits(patterns).items():
        unused = set(digit_segments) - mapped_segments
        for wire in wires:
            if wire not in mapping:
                mapping[wire] = list(unused)
        mapped_segments |= unused

    return {k: v for k, v in sorted(mapping.items())}


def fix_digit(segments: str, mapping: Dict[str, str]) -> str:
    """Translate scrambled string of segments to display digit."""
    return "".join(sorted(segments.translate(str.maketrans(mapping))))  # type: ignore


def is_digit_valid(segments: str) -> bool:
    """Check if string of segments represents correct display digit."""
    return segments in DIGITS


def wires_to_correct_segments(patterns: List[str]) -> Dict[str, str]:
    """Return mapping of each control wire to correct segment."""
    mapping = wires_to_possible_segments(patterns)
    for segments in itertools.product(*mapping.values()):
        single_segment_mapping = dict(zip(WIRES, segments))
        for pattern in patterns:
            digit = fix_digit(pattern, single_segment_mapping)
            if not is_digit_valid(digit):
                break
        else:
            return single_segment_mapping
    return {}


def patterns_to_ints(patterns: List[str], mapping: Dict[str, str]) -> List[int]:
    """Convert list of scrambled segments to integers."""
    ints = []
    for pattern in patterns:
        ints.append(DIGITS[fix_digit(pattern, mapping)])

    return ints


def get_number(entry: TEntry) -> int:
    """Decode entry to number that's supposed to be on the display."""
    patterns, digits = entry
    mapping = wires_to_correct_segments(patterns)
    ints = patterns_to_ints(digits, mapping)

    result = ints[0]
    for n in ints[1:]:
        result *= 10
        result += n

    return result


def get_sum(entries: List[TEntry]) -> int:
    """Get sum of all decoded numbers."""
    return sum(get_number(entry) for entry in entries)


def count_easy_digits(entries: List[TEntry]) -> int:
    """Get number of easy digits among entries."""
    count = 0
    for _, digits in entries:
        for digit in digits:
            if len(digit) in EASY_DIGITS_LENGTHS:
                count += 1

    return count


def parse_input(file: str = "input.txt") -> List[TEntry]:
    entries = []
    with open(file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            patterns, digits = line.split(" | ")
            entries.append((patterns.split(), digits.split()))

    return entries


if __name__ == "__main__":
    lines = parse_input("input.txt")
    for idx, solution in enumerate([count_easy_digits(lines), get_sum(lines)]):
        print(f"Solution {idx + 1}: {solution:6}")  # 367, 974512
