"""Advent of Code - Day 4."""

from pathlib import Path
from typing import List, Tuple

FILE_PATH = Path(__file__).parent.parent / "data" / "day_4.txt"


def sum_redundant_ranges(pairs: List, type: str) -> int:
    """Range overlap.

    Sum up fully contained or overlapping ranges.

    Args:
        pairs: List of range limits for each pair.
        type: 'fully' to sum up fully contained ranges only, else any overlap counts.

    Returns:
        int: Total number of ranges that are fully contained / overlapping dependending on type.
    """

    def get_ranges(pair: List) -> Tuple:
        first, second = [x.split("-") for x in pair]
        first_range, second_range = [
            set(range(int(x[0]), int(x[1]) + 1)) for x in [first, second]
        ]
        return first_range, second_range

    def is_contained(pair: List) -> bool:
        first_range, second_range = get_ranges(pair)
        return first_range.issubset(second_range) or first_range.issuperset(
            second_range
        )

    def has_overlap(pair: List) -> bool:
        first_range, second_range = get_ranges(pair)
        return not first_range.isdisjoint(second_range)

    sum_pairs = 0

    for pair in pairs:
        sum_pairs += is_contained(pair) if type == "fully" else has_overlap(pair)

    return sum_pairs


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        pairs = [line.strip().split(",") for line in file.readlines()]

    print(f"Part 1: {sum_redundant_ranges(pairs, type='fully')}.")
    print(f"Part 2: {sum_redundant_ranges(pairs, type='overlap')}.")
