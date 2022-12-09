"""Advent of Code - Day 9."""

from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_9.txt"


def simulate(moves: list, n: int) -> list:
    """Simulation.

    Simulate rope movements with n knots.

    Args:
        moves: List of puzzle input. Each item is a tuple where the first item
            indicates the direciton and the second item the step size.
        n: Number of knots.

    Returns:
        list: Positions for each knot.
    """
    knots = [(0, 0) for _ in range(n)]
    positions = [[] for _ in range(n)]

    def follow_head(tail: tuple, head: tuple) -> tuple:
        if sum((x - y) ** 2 for x, y in zip(tail, head)) <= 2:
            return tail
        positions = [
            (i, j)
            for i in [head[0] - 1, head[0], head[0] + 1]
            for j in [head[1] - 1, head[1], head[1] + 1]
            if (i, j) != head
        ]
        # at most one step vertical and/or horizontal possible
        available_positions = [
            pos
            for pos in positions
            if abs(tail[0] - pos[0]) <= 1 and abs(tail[1] - pos[1]) <= 1
        ]
        distance = [
            (head[0] - pos[0]) ** 2 + (head[1] - pos[1]) ** 2
            for pos in available_positions
        ]
        [tail] = [
            pos
            for i, pos in enumerate(available_positions)
            if distance[i] == min(distance)
        ]

        return tail

    for move, step in moves:
        for _ in range(step):
            for i in range(len(knots) - 1):
                head, tail = knots[i], knots[i + 1]
                if i == 0:
                    if move == "U":
                        head = (head[0] + 1, head[1])
                    elif move == "D":
                        head = (head[0] - 1, head[1])
                    elif move == "R":
                        head = (head[0], head[1] + 1)
                    elif move == "L":
                        head = (head[0], head[1] - 1)

                tail = follow_head(tail, head)
                knots[i], knots[i + 1] = head, tail
                positions[i + 1].append(tail)

    return positions


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [line.strip().split() for line in file.readlines()]
    moves = [(line[0], int(line[1])) for line in lines]
    print(f"Part 1: {len(set(simulate(moves, n=2)[-1]))}.")
    print(f"Part 2: {len(set(simulate(moves, n=10)[-1]))}.")
