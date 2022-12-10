"""Advent of Code - Day 10."""

from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_10.txt"


def _compute_x_register(signals: list) -> list:
    """X register.

    Compute the value of the X register after each cycle.

    Args:
        signals: Signals sent by CPU (puzzle input).

    Returns:
        list: Value of the X register after each cycle.

    Raises:
        ValueError: If signal does not match 'noop' or 'addx V'.
    """
    x = [1, 1]
    for signal in signals:
        match signal:
            case ["noop"]:
                x.append(x[-1])
            case ["addx", register]:
                x.extend([x[-1] + int(register) for _ in range(2)])
            case _:
                raise ValueError("Invalid signal.")

    return x


def compute_signal_strength(signals: list, cycles: list[int]) -> list:
    """Signal strenghts.

    Value of the X register during the ith cycle multiplied by the cycle
    number.

    Args:
        signals: Signals sent by CPU (puzzle input).
        cycles: Cycle numbers.

    Returns:
        list: Register values multiplied by cycle numbers.
    """
    x = _compute_x_register(signals)
    # x[i] is the value of x after the ith cycle
    return [x[i - 1] * i for i in cycles]


def draw_pixels(signals: list) -> str:
    """CRT image.

    Use X register values as midpoints for sprite to draw the CRT image.

    Args:
        signals: Signals sent by CPU (puzzle input).

    Returns:
        str: Pixels to print.
    """
    x = _compute_x_register(signals)
    pixels = []

    shifts = [i * 40 for i in range(7)]
    for i, center in enumerate(x):
        shift = max([j for j in shifts if j <= i])
        pos = i - shift
        pixel = "#" if center - 1 <= pos <= center + 1 else "."
        pixels.append(pixel)

    return "\n".join(["".join(pixels[(i * 40) : ((i + 1) * 40)]) for i in range(6)])


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        signals = [line.strip().split() for line in file.readlines()]
    print(
        f"Part 1: {sum(compute_signal_strength(signals, cycles=[20, 60, 100, 140, 180, 220]))}."
    )
    print(f"Part 2:\n{draw_pixels(signals)}")
