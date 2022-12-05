"""Advent of Code - Day 5."""
import re
from collections import deque
from pathlib import Path
from typing import Deque, Dict, List

FILE_PATH = Path(__file__).parent.parent / "data" / "day_5.txt"


def arrange_crates(crates: List, procedure: List, is_new_version: bool) -> str:
    """Supply stacks.

    Move crates with the CrateMover 9000 and 9001.

    Args:
        crates: List of crates.
        procedure: List of steps for rearrangement.
        is_new_version: Should the CrateMover 9001 be used?

    Returns:
        str: Crates on top of each stack.
    """
    index = crates[-1]
    crates = crates[:-1]
    stacks: Dict[str, Deque] = {i: deque() for i in index.split()}

    for row in reversed(crates):
        for n, crate in zip(index, re.sub(r"\[|\]", " ", row).strip()):
            if len(crate.strip()) > 0:
                stacks[n].append(crate)

    for step in procedure:
        n, from_stack, to_stack = re.findall(r"\d+", step)
        batch = []
        for _ in range(int(n)):
            batch.append(stacks[from_stack].pop())

        if is_new_version:
            batch.reverse()

        stacks[to_stack].extend(batch)

    return "".join([stack.pop() for stack in stacks.values()])


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    [split] = [i for i, line in enumerate(lines) if line == ""]
    crates, procedure = lines[:split], lines[(split + 1) :]
    print(f"Part 1: {arrange_crates(crates, procedure, is_new_version=False)}.")
    print(f"Part 2: {arrange_crates(crates, procedure, is_new_version=True)}.")
