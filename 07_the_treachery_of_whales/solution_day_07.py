"""https://adventofcode.com/2021/day/7"""

from typing import List, Callable

TCostFunc = Callable[[List[int], int], int]


def fuel_to_point_1(crabs: List[int], point: int) -> int:
    """Calculate how much fuel all crabs burn to get to the given point.

    Consumption as for part 1.
    """
    fuel = 0
    for crab in crabs:
        fuel += abs(crab - point)

    return fuel


def fuel_to_point_2(crabs: List[int], point: int) -> int:
    """Calculate how much fuel all crabs burn to get to the given point.

    Consumption as for part 2.
    """
    fuel = 0
    for crab in crabs:
        distance = abs(crab - point)
        fuel += distance * (distance + 1) // 2

    return fuel


def find_lowest_consumption(
    crabs: List[int], distance_min: int, distance_max: int, cost_func: TCostFunc
) -> int:
    """Find and return the lowest possible fuel consumption.

    Using kind of binary search.
    """
    mid = (distance_max + distance_min) // 2
    left = mid - 1
    right = mid + 1

    cost_mid = cost_func(crabs, mid)
    cost_left = cost_right = float("inf")
    if left >= distance_min:
        cost_left = cost_func(crabs, left)
    if right <= distance_max:
        cost_right = cost_func(crabs, right)

    if cost_right < cost_mid:
        return find_lowest_consumption(crabs, right, distance_max, cost_func)
    if cost_left < cost_mid:
        return find_lowest_consumption(crabs, distance_min, left, cost_func)
    return cost_mid


def parse_input(file: str = "input_example.txt") -> List[int]:
    with open(file, "r", encoding="utf-8") as fh:
        return [int(n) for n in next(fh).strip().split(",")]


if __name__ == "__main__":
    crabs = parse_input("input.txt")
    min_crab = min(crabs)
    max_crab = max(crabs)

    for idx, func in enumerate([fuel_to_point_1, fuel_to_point_2]):
        burned = find_lowest_consumption(crabs, min_crab, max_crab, func)
        print(f"Solution {idx + 1}: {burned:8}")  # 348996, 98231647
