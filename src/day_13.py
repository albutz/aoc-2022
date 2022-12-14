"""Advent of Code - Day 13."""

from collections import deque
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_13.txt"

# FILE_PATH = Path().cwd() / "test.txt"


def parse_packets(lines: list[str]) -> list:
    split_points = [i for i, val in enumerate(lines) if val == ""]
    split_points.insert(0, -1)
    split_points.append(len(lines))

    signals = [
        lines[(split_points[i] + 1) : split_points[i + 1]]
        for i in range(len(split_points) - 1)
    ]

    return signals


def compare_packet(packet: list[str]):

    left, right = [deque(eval(p)) for p in packet]

    def _compare(l, r):
        # One list starts empty
        if len(l) == 0:
            print("Left side ran out of items.")
            return True
        if len(r) == 0:
            print("Right side ran out of items.")
            return False
        l, r = deque(l), deque(r)
        for l_, r_ in zip(l, r):
            match (l_, r_):
                case (int(l__), int(r__)):
                    print(f"Case 1: {l__=}, {r__=}")
                    # Int comparison
                    if l__ != r__:
                        return True if l__ < r__ else False
                    # One side runs out of items
                    # elif len(left) != len(right):
                    #     side = "Left" if len(left) < len(right) else "Right"
                    #     print(f"{side} side ran out of items.")
                    #     return len(left) < len(right)
                    else:
                        continue
                case (list(l__), list(r__)):
                    print(f"Case 2: {l__=}, {r__=}")
                    return _compare(l_, r_)
                case (list(l__), int(r__)):
                    print(f"Case 3: {l__=}, {r__=}")
                    return _compare(l__, [r__])
                case (int(l__), list(r__)):
                    print(f"Case 4: {l__=}, {r__=}")
                    return _compare([l__], r__)

        print("loop exited")

        # One side runs out of items
        if len(left) != len(right):
            side = "Left" if len(left) < len(right) else "Right"
            print(f"{side} side ran out of items.")
            return len(left) < len(right)

        # Drop current item (list) and start again
        left.popleft()
        right.popleft()

        return _compare(left, right)

    return _compare(left, right)


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    packets = parse_packets(lines)
    print(
        f"Part 1: {sum([i + 1 for i, packet in enumerate(packets) if compare_packet(packet)])}."
    )
