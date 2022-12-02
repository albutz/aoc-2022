"""Advent of Code - Day 1."""
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_1.txt"


def find_elves_most_calories(calories: Path | str, n: int) -> int:
    """Fat elf detection.

    Find the elf carrying the most calories.

    Args:
        calories: Input file for puzzle.
        n: Threshold for top n elves by calories.

    Returns:
        int: Total calories for top n elves.
    """
    with open(calories, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    line_breaks = [int(i) for i, line in enumerate(lines) if line == ""]

    # inner groups
    elves = [
        lines[(line_breaks[i] + 1) : line_breaks[i + 1]]
        for i, _ in enumerate(line_breaks[:-1])
    ]

    # outer groups
    elves.insert(0, lines[: line_breaks[0]])
    elves.append(lines[(line_breaks[-1] + 1) :])

    # Sum per elf (tuple with elf number first, sum of calories second)
    cals = [(num + 1, sum([int(cal) for cal in elf])) for num, elf in enumerate(elves)]
    # Sort by calories
    cals.sort(key=lambda x: x[-1], reverse=True)

    # Sum top n calories
    return sum([cal for _, cal in cals[:n]])


if __name__ == "__main__":
    print(f"Part 1: {find_elves_most_calories(calories=FILE_PATH, n=1)}.")
    print(f"Part 2: {find_elves_most_calories(calories=FILE_PATH, n=3)}.")
