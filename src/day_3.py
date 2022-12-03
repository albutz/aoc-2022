"""Advent of Code - Day 3."""

import string
from pathlib import Path
from typing import List, Tuple

FILE_PATH = Path(__file__).parent.parent / "data" / "day_3.txt"

priority_lookup = {
    letter: priority + 1 for priority, letter in enumerate(string.ascii_letters)
}


def sum_compartment_priorities(rucksacks: List) -> int:
    """Compartment priorities.

    Args:
        rucksacks: List with puzzle input.

    Returns:
        int: Sum of priorities by compartment item.
    """

    def find_item(items: str) -> str:
        split = int(len(items) / 2)
        first_compartment = set(items[:split])
        second_compartment = set(items[split:])
        return first_compartment.intersection(second_compartment).pop()

    priority_sum = 0
    for rucksack in rucksacks:
        priority_sum += priority_lookup[find_item(rucksack)]

    return priority_sum


def sum_group_priorities(rucksacks: List) -> int:
    """Badge priorities.

    Args:
        rucksacks: List with puzzle input.

    Returns:
        int: Sum of badge priorites.
    """

    def find_item(group: Tuple) -> str:
        first, second, third = [set(x) for x in group]
        return first.intersection(second).intersection(third).pop()

    groups = [
        (first, second, third)
        for first, second, third in zip(
            rucksacks[::3], rucksacks[1::3], rucksacks[2::3]
        )
    ]

    badge_priority_sum = 0
    for group in groups:
        badge_priority_sum += priority_lookup[find_item(group)]

    return badge_priority_sum


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        rucksacks = [line.strip() for line in file.readlines()]

    print(f"Part 1: {sum_compartment_priorities(rucksacks)}.")
    print(f"Part 2: {sum_group_priorities(rucksacks)}.")
