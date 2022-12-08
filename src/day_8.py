"""Advent of Code - Day 8."""

from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_8.txt"


def get_aligned_trees(trees: list, i: int, j: int) -> tuple:
    """Aligned trees.

    Get left, right, top and bottom trees to the tree in row i, column j.

    Args:
        trees: List of tree heights.
        i: Row number.
        j: Column number.

    Returns:
        tuple: Left, right, top and bottom trees.
    """
    left = trees[i][:j]
    right = trees[i][(j + 1) :]
    top = [row[j] for row in trees[:i]]
    bottom = [row[j] for row in trees[(i + 1) :]]

    return left, right, top, bottom


def count_trees(trees: list) -> int:
    """Count trees.

    Calculate the number of visible trees from outside the grid.

    Args:
        trees: List of tree heights.

    Returns:
        int: Number of visible trees.
    """
    n_rows = len(trees)
    n_cols = len(trees[0])

    # edge
    visible_trees = 2 * n_rows + 2 * n_cols - 4
    # inner
    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            tree = trees[i][j]

            left, right, top, bottom = get_aligned_trees(trees, i, j)

            left_visible = all(tree > left for left in left)
            right_visible = all(tree > right for right in right)
            top_visible = all(tree > top for top in top)
            bottom_visible = all(tree > bottom for bottom in bottom)

            visible_trees += (
                left_visible or right_visible or top_visible or bottom_visible
            )

    return visible_trees


def find_max_scenic_score(trees: list) -> int:
    """Scenic score.

    For each tree, compute the number of trees that are in view to the left,
    right, top and bottom. Multiple the number of trees in view in each
    direction to get the scenic score of that tree.

    Args:
        trees: List of tree heights.

    Returns:
        int: Maximum scenic score.
    """

    def _get_viewing_distance(tree: int, tree_line: list, reverse: bool) -> int:
        if len(tree_line) == 0:
            return 0

        if reverse is True:
            tree_line = list(reversed(tree_line))

        viewing_distance = 0
        for other_tree in tree_line:
            viewing_distance += 1
            if other_tree >= tree:
                break

        return viewing_distance

    n_rows = len(trees)
    n_cols = len(trees[0])

    scenic_scores = []
    for i in range(n_rows):
        for j in range(n_cols):
            tree = trees[i][j]

            left, right, top, bottom = get_aligned_trees(trees, i, j)

            score = (
                _get_viewing_distance(tree, left, reverse=True)
                * _get_viewing_distance(tree, right, reverse=False)
                * _get_viewing_distance(tree, top, reverse=True)
                * _get_viewing_distance(tree, bottom, reverse=False)
            )

            scenic_scores.append(score)

    return max(scenic_scores)


if __name__ == "__main__":
    with open(FILE_PATH, "r") as file:
        lines = [list(line.strip()) for line in file.readlines()]
    trees = [[int(tree) for tree in line] for line in lines]
    print(f"Part 1: {count_trees(trees)}.")
    print(f"Part 2: {find_max_scenic_score(trees)}.")
