"""Advent of Code - Day 6."""
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_6.txt"


def detect_start_of_packet(stream: str, n: int) -> int:
    """Start-of-packet.

    Compute the number of characters before the first group of n distinct
    characters in the datastream.

    Args:
        stream: Device datastream.
        n: Number of distinct characters.

    Returns:
        int: Number of characters before first start-of-packet.
    """
    for pos, _ in enumerate(stream, start=n):
        signals = stream[(pos - n) : pos]
        if len(set(signals)) == n:
            return pos  # need number of characters before first start-of-packet

    return -1


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        stream = file.read().strip()
    print(f"Part 1: {detect_start_of_packet(stream, n=4)}.")
    print(f"Part 2: {detect_start_of_packet(stream, n=14)}.")
