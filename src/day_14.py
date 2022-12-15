"""Advent of Code - Day 14."""

from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_14.txt"


def simulate_sand(rocks: list, has_bottom: bool) -> int:
    """Sand.

    Simulate sand falling in the cave.

    Args:
        rocks: Formatted puzzle input.
        has_bottom: Whether the cave has a bottom line or not.

    Returns:
        int: Number of sand grains.
    """
    scan = simulate_rocks(rocks)
    max_y = max(x[1] for x in scan)
    bottom_y = max_y + 2 if has_bottom else max_y

    if has_bottom:
        bottom = set([(-i, bottom_y) for i in range(10_000)]).union(
            set([(i, bottom_y) for i in range(10_000)])
        )
        scan = scan.union(bottom)

    counter = 0
    no_overflow = True
    while no_overflow:
        counter += 1
        pos = (500, 0)
        while True:

            if has_bottom:
                if ((500, 1) in scan) and ((501, 1) in scan) and ((499, 1) in scan):
                    no_overflow = False
                    break
            else:
                # overflow
                if pos[1] > max_y:
                    no_overflow = False
                    break

            step_down = not (pos_down := (pos[0], pos[1] + 1)) in scan
            if step_down:
                pos = pos_down
            else:
                step_left_diagonal = (
                    not (pos_left_diagonal := (pos[0] - 1, pos[1] + 1)) in scan
                )
                if step_left_diagonal:
                    pos = pos_left_diagonal
                else:
                    step_right_diagonal = (
                        not (pos_right_diagonal := (pos[0] + 1, pos[1] + 1)) in scan
                    )
                    if step_right_diagonal:
                        pos = pos_right_diagonal
                    else:
                        scan.add(pos)
                        break

    return counter if has_bottom else counter - 1


def simulate_rocks(rocks: list) -> set:
    """Rocks.

    Simulate rocks falling in the cave.

    Args:
        rocks: Formatted puzzle input.

    Returns:
        set: Coordinates of rocks.
    """
    scan = []

    for rock in rocks:
        for i, _ in enumerate(rock):
            x_prev, y_prev = rock[i - 1] if i > 0 else rock[i]
            x_prev, y_prev = int(x_prev), int(y_prev)
            x_curr, y_curr = rock[i]
            x_curr, y_curr = int(x_curr), int(y_curr)

            if x_curr != x_prev:
                x_start = x_curr if x_curr < x_prev else x_prev
                x_move = abs(x_curr - x_prev)
                path = [(x_start + i, y_curr) for i in range(x_move + 1)]
            else:
                y_start = y_curr if y_curr < y_prev else y_prev
                y_move = abs(y_curr - y_prev)
                path = [(x_curr, y_start + i) for i in range(y_move + 1)]

            scan.extend(path)

    return set(scan)


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    rocks = [
        [tuple(coords.strip().split(",")) for coords in line.split("->")]
        for line in lines
    ]
    print(f"Part 1: {simulate_sand(rocks, has_bottom=False)}.")
    print(f"Part 2: {simulate_sand(rocks, has_bottom=True)}.")
