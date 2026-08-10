from __future__ import annotations

from random import Random


def choose_move(
    turn: int,
    my_history: str,
    opponent_history: str,
    rng: Random,
) -> str:
    """Choose this turn's move; the only valid results are R, P, and S.

    ``turn`` starts at 1. The history strings contain the earlier moves in
    oldest-to-newest order. Use ``rng`` for every random decision so that the
    Tournament can reproduce the strategy's behavior from its seed.
    """

    return rng.choice(("R", "P", "S"))
