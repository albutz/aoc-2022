"""Advent of Code - Day 2."""
from __future__ import annotations

from pathlib import Path

FILE_PATH = Path(__file__).parent.parent / "data" / "day_2.txt"


class Move:
    """Rock, paper, scissors move."""

    _moves_lookup = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissors",
    }

    def __init__(self, move: str):
        """Initialize move.

        Args:
            move: str that specifies move.
        """
        self.move = self._moves_lookup[move]

    def __eq__(self, other: object) -> bool:
        """Check if there's a tie.

        Args:
            other: Move of the opponent.

        Returns:
            bool: True if there's a tie, else False.
        """
        if not isinstance(other, Move):
            return NotImplemented

        return self.move == other.move

    def __lt__(self, other: Move) -> bool:
        """Check if the second player wins.

        Args:
            other: Move of the opponent.

        Returns:
            bool indicating if second player wins.
        """
        moves = (self.move, other.move)
        match moves:
            case ("Rock", "Paper"):
                return True
            case ("Paper", "Scissors"):
                return True
            case ("Scissors", "Rock"):
                return True
            case _:
                return False

    def __gt__(self, other: Move) -> bool:
        """Check if the first player wins.

        Args:
            other: Move of the opponent.

        Returns:
            bool indicating if second player wins.
        """
        return not self < other and not self == other


def compute_total_score(strategy_guide: Path | str, type: str) -> int:
    """Total score.

    Computation of total score with strategy input.

    Args:
        strategy_guide: Input file for puzzle.
        type: Type of instruction. If 'result', then X / Y / Z indicate
              loss / draw / win, else rock / paper / scissors.

    Returns:
        int: Total score.
    """
    with open(strategy_guide, "r") as file:
        strategy = [line.strip().split() for line in file.readlines()]

    # 6 for win, 3 for draw, points for shape
    def compute_points(opponent: Move, own: Move) -> int:
        _shape_points = {"Rock": 1, "Paper": 2, "Scissors": 3}
        return (opponent < own) * 6 + (opponent == own) * 3 + _shape_points[own.move]

    # X = Lose, Y = Draw, Z = Win
    def get_own_move(opponent: Move, result: str) -> Move:
        for own in ["X", "Y", "Z"]:
            if result == "X":
                if opponent > Move(own):
                    return Move(own)
            elif result == "Y":
                if opponent == Move(own):
                    return Move(own)
            elif result == "Z":
                if opponent < Move(own):
                    return Move(own)
        # Default move
        return Move("X")

    points = 0
    for moves in strategy:
        opponent = Move(moves[0])
        own = get_own_move(opponent, moves[1]) if type == "result" else Move(moves[1])
        points += compute_points(opponent, own)

    return points


if __name__ == "__main__":
    print(f"Part 1: {compute_total_score(FILE_PATH, 'move')}")
    print(f"Part 2: {compute_total_score(FILE_PATH, 'result')}")
