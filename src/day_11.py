"""Advent of Code - Day 11."""

import re
from collections import deque
from functools import reduce
from math import lcm
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_11.txt"


def fmt_puzzle_input(notes: list[str]) -> list:
    """Formatting.

    Split puzzle input to lists of monkeys.

    Args:
        notes: Raw puzzle input.

    Returns:
        list: List of notes for each monkey.
    """
    split_points = [i for i, val in enumerate(notes) if val == ""]
    split_points.insert(0, -1)
    split_points.append(len(notes))

    monkey_list = [
        notes[(split_points[i] + 2) : split_points[i + 1]]
        for i in range(len(split_points) - 1)
    ]

    return monkey_list


def get_monkeys(monkey_list: list) -> list:
    """Parse monkeys.

    Get items of each monkey as a deque, the operation to be applied as a
    function and the integer for the division check and monkey indices to pass
    the item to in a dict.

    Args:
        monkey_list: Formatted puzzle input.

    Returns:
        list: List of monkeys.
    """
    monkeys = []
    r = re.compile(r"\d+")

    for monkey in monkey_list:
        items = deque(
            [int(item) for item in monkey[0].removeprefix("Starting items:").split(",")]
        )
        operation = monkey[1].removeprefix("Operation: new =").strip()
        operation = eval(f"lambda old: {operation}")
        divisible_by = int(*re.findall(r, monkey[2]))
        if_true = int(*re.findall(r, monkey[3]))
        if_false = int(*re.findall(r, monkey[4]))
        monkeys.append(
            {
                "items": items,
                "operation": operation,
                "divisible_by": divisible_by,
                "if_true": if_true,
                "if_false": if_false,
            }
        )

    return monkeys


def track_monkeys(notes: list, n_rounds: int, worry_drop: bool) -> list[int]:
    """Count items.

    Count items of each monkey for n rounds. Divide the worry level by 3 if
    worry_drop is true, else shift by the LCM of all monkey dividers if the
    worry levels get too big.

    Args:
        notes: Raw puzzle input.
        n_rounds: Number of rounds.
        worry_drop: Boolean indicating if worry levels should be divided by 3
                    after item inspection by a monkey.

    Returns:
        list[int]: Item counts for each monkey.
    """
    notes_fmt = fmt_puzzle_input(notes)
    monkeys = get_monkeys(notes_fmt)
    # shift by lcm if int gets too big
    limiter = lcm(*[monkey["divisible_by"] for monkey in monkeys])

    counts = [0 for _ in range(len(monkeys))]
    for _ in range(n_rounds):
        for i, monkey in enumerate(monkeys):
            counts[i] += len(monkey["items"])
            for _ in range(len(monkey["items"])):
                item = monkey["items"].popleft()
                # apply operation
                item = monkey["operation"](item)

                # divide
                if worry_drop:
                    item = item // 3
                else:
                    if item > limiter:
                        item = item % limiter

                test_passes = (item % monkey["divisible_by"]) == 0
                to_monkey = monkey["if_true"] if test_passes else monkey["if_false"]
                monkeys[to_monkey]["items"].append(item)

    return counts


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        notes = [line.strip() for line in file.readlines()]
    counts_part_1 = track_monkeys(notes, n_rounds=20, worry_drop=True)
    counts_part_2 = track_monkeys(notes, n_rounds=10_000, worry_drop=False)
    print(
        f"Part 1: {reduce(lambda x, y: x*y, sorted(counts_part_1, reverse=True)[:2])}"
    )
    print(
        f"Part 2: {reduce(lambda x, y: x*y, sorted(counts_part_2, reverse=True)[:2])}"
    )
