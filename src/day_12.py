"""Advent of Code - Day 12."""

import string
from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_12.txt"


def _get_coordinates(heatmap: list, point: str) -> list[tuple]:
    """Coordinates.

    Get a list of coordinates for points of a specific field.

    Args:
        heatmap: Formatted puzzle input.
        point: Field value.

    Returns:
        list[tuple]: Coordinates on the heatmap with the specified value.
    """
    coordinates = [
        (i, j)
        for i, row in enumerate(heatmap)
        for j, val in enumerate(row)
        if val == point
    ]
    return coordinates


def _get_value(x: str) -> int:
    """Height for a field value.

    Args:
        x: Field value.

    Returns:
        int: Height.
    """
    if x == "S":
        return 0
    elif x == "E":
        return len(string.ascii_lowercase) - 1

    [index] = [i for i, val in enumerate(string.ascii_lowercase) if val == x]
    return index


def _is_reachable(current: str, next: str) -> bool:
    """Reachable.

    Check if next is reachable from current regarding the height difference.

    Args:
        current: Current field value.
        next: Next field value.

    Returns:
        bool: Whether next is reachable or not.
    """
    match (current, next):
        case ("S", n):
            current_height = 0
            next_height = _get_value(n)
        case (c, "E"):
            current_height = _get_value(c)
            next_height = len(string.ascii_lowercase) - 1
        case (c, n):
            current_height = _get_value(c)
            next_height = _get_value(n)

    return next_height - current_height <= 1


def _get_reachable_points(heatmap: list, pos: tuple) -> list[tuple]:
    """Reachable neighbors.

    Get a list of coordinates that are reachable from the current position.

    Args:
        heatmap: Formatted puzzle input.
        pos: Current position.

    Returns:
        list[tuple]: List of reachable neighbors.
    """
    points = []
    i_current, j_current = pos
    for i_next, j_next in [
        (i_current - 1, j_current),
        (i_current + 1, j_current),
        (i_current, j_current + 1),
        (i_current, j_current - 1),
    ]:
        if (
            (i_next == -1)
            or (j_next == -1)
            or (i_next == len(heatmap))
            or (j_next == len(heatmap[0]))
        ):
            continue
        if not _is_reachable(heatmap[i_current][j_current], heatmap[i_next][j_next]):
            continue
        points.append((i_next, j_next))
    return points


def find_path(heatmap: list, low_elevation: bool) -> list:
    """Shortest path.

    BFS algorithm to find the shortest path. If low_elevation is true, then all
    possible starting points with minimal height are considered.

    Args:
        heatmap: Formatted puzzle input.
        low_elevation: Should all starting points with minimal height be
                       considered?

    Returns:
        list: List of path lengths.
    """

    def _get_mappings(heatmap: list) -> tuple:
        graph = {}
        visited = {}
        prev_points = {}
        n_rows = len(heatmap)
        n_cols = len(heatmap[0])
        for i in range(n_rows):
            for j in range(n_cols):
                graph[(i, j)] = _get_reachable_points(heatmap, (i, j))
                visited[(i, j)] = False
                prev_points[(i, j)] = None

        return graph, visited, prev_points

    initial_start = _get_coordinates(heatmap, "S")
    if not low_elevation:
        starting_points = initial_start
    else:
        starting_points = _get_coordinates(heatmap, "a")
        starting_points.extend(initial_start)
    [end_point] = _get_coordinates(heatmap, "E")

    opt_paths = []

    for start_point in starting_points:
        graph, visited, prev_points = _get_mappings(heatmap)
        visited[start_point] = True
        queue = [start_point]

        while queue:
            current_point = queue.pop(0)
            neighbors = graph[current_point]

            for neighbor in neighbors:
                if visited[neighbor] is False:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    prev_points[neighbor] = current_point

        opt_path = []
        prev = end_point

        # Case if starting point has no solution
        if prev_points[prev] is None:
            continue

        while True:
            prev = prev_points[prev]
            if prev is None:
                break
            opt_path.append(prev)

        opt_paths.append(list(reversed(opt_path)))

    return opt_paths


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    heatmap = [[e for e in line] for line in lines]
    print(f"Part 1: {len(find_path(heatmap, low_elevation=False)[0])}.")
    print(f"Part 2: {min([len(p) for p in find_path(heatmap, low_elevation=True)])}.")
