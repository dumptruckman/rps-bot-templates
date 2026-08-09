from __future__ import annotations

from random import Random


def choose_move(
    turn: int,
    my_history: str,
    opponent_history: str,
    rng: Random,
) -> str:
    """Return Rock, Paper, or Scissors using wrapper-provided randomness."""

    return rng.choice(("R", "P", "S"))
