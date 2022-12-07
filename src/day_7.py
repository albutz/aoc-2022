"""Advent of Code - Day 7."""

import re
from copy import deepcopy
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_7.txt"


def construct_tree(terminal_output: list[str]) -> tuple[dict, list]:
    """File tree.

    Iterate through the terminal output and build the file tree and the jump
    list.

    Args:
        terminal_output: Puzzle input split by line.

    Returns:
        tuple[dict, list]: Tree and jump list.
    """
    tree = {}  # type: ignore
    node = tree
    pos = []
    jump_list = []
    for line in terminal_output:
        if re.search(r"^\$ cd [/a-zA-Z]", line):
            dir_name = line.removeprefix("$ cd").strip()
            node[dir_name] = {}
            node = node[dir_name]
            node["files"] = []
            pos.append(dir_name)
            if pos not in jump_list:
                jump_list.append(deepcopy(pos))
        elif line.startswith("dir"):
            dir_name = line.removeprefix("dir").strip()
            node[dir_name] = {}
        elif re.search(r"^[0-9]", line):
            node["files"].append(int(line.split()[0]))
        elif line == "$ cd ..":
            pos.pop(-1)
            if pos not in jump_list:
                jump_list.append(deepcopy(pos))
            node = tree
            for dir_name in pos:
                node = node[dir_name]

    return tree, jump_list


def compute_sizes(tree: dict, jump_list: list) -> dict:
    """Directory sizes.

    Args:
        tree: File tree.
        jump_list: Jump list from cd moves.

    Returns:
        dict: Size of each directory, keys from jump list.
    """

    def _compute_size(directory: dict) -> int:
        size = 0
        for key, vals in directory.items():
            if key == "files":
                size += sum(vals)
            else:
                size += _compute_size(vals)

        return size

    sizes = {}
    for d in jump_list:
        node = tree
        for sub_d in d:
            node = node[sub_d]
        sizes[" ".join(d)] = _compute_size(node)

    return sizes


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        terminal_output = [line.strip() for line in file.readlines()]
    tree, jump_list = construct_tree(terminal_output)
    sizes = compute_sizes(tree, jump_list)
    small_dirs = [size for _, size in sizes.items() if size < 100000]
    required_space = 30000000 - (70000000 - sizes["/"])
    available_dirs = [size for _, size in sizes.items() if size >= required_space]
    print(f"Part 1: {sum(small_dirs)}")
    print(f"Part 2: {min(available_dirs)}")
