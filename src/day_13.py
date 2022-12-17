"""Advent of Code - Day 13."""

from functools import reduce
from itertools import zip_longest
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_13.txt"


def parse_packets(lines: list[str]) -> list:
    """Parsing.

    Parse pairs of packets from signals.

    Args:
        lines: Puzzle input.

    Returns:
        list: List of pairs for comparison.
    """
    split_points = [i for i, val in enumerate(lines) if val == ""]
    split_points.insert(0, -1)
    split_points.append(len(lines))

    signals = [
        lines[(split_points[i] + 1) : split_points[i + 1]]
        for i in range(len(split_points) - 1)
    ]

    return [[eval(p[0]), eval(p[1])] for p in signals]


def compare_packet(left: int | list, right: int | list) -> int:
    """Comparison.

    Compare two packets. Returns a positive integer if the pairs are in the
    right order an a negative integer if they are in the reverse order.

    Args:
        left: Left item for comparison.
        right: Right item for comparison.

    Returns:
        int: Order indicator.
    """
    # > 0 if in right order
    match (left, right):
        case (int(l), int(r)):
            return r - l
        case (int(l), list(r)):
            return compare_packet([l], r)
        case (list(l), int(r)):
            return compare_packet(l, [r])
        case (list(l), list(r)):
            for l_, r_ in zip_longest(l, r):
                if l_ is None:
                    return 1
                elif r_ is None:
                    return -1
                elif diff := compare_packet(l_, r_):
                    return diff
    return 0


def compute_decoder_key(packets: list) -> int:
    """Decoder key.

    Sort all packets and return the decoder key for the divider packets.

    Args:
        packets: List of pairs for comparison.

    Returns:
        int: Decoder key.
    """
    # Initialize with divider packets
    sorted_packets = [[[2]], [[6]]]
    for packet in packets:
        for p in packet:
            for i, sorted_packet in enumerate(sorted_packets):
                if compare_packet(sorted_packet, p) <= 0:
                    sorted_packets.insert(i, p)
                    break
    divider_indices = [
        i
        for i, packet in enumerate(sorted_packets, 1)
        if packet == [[2]] or packet == [[6]]
    ]
    return reduce(lambda x, y: x * y, divider_indices)


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    packets = parse_packets(lines)
    sum_of_indices = sum(
        [
            i
            for i, packet in enumerate(packets, 1)
            if compare_packet(packet[0], packet[1]) > 0
        ]
    )
    print(f"Part 1: {sum_of_indices}.")
    decoder_key = compute_decoder_key(packets)
    print(f"Part 2: {decoder_key}.")
