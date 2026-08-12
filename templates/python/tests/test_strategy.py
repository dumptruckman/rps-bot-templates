from __future__ import annotations

import inspect
from pathlib import Path
import random
import sys
import unittest


TEAM_SOURCE = Path(__file__).resolve().parents[1] / "team_source"
sys.path.insert(0, str(TEAM_SOURCE))

import strategy  # noqa: E402


class StarterStrategyTests(unittest.TestCase):
    def test_strategy_implements_the_four_argument_contract(self) -> None:
        self.assertEqual(
            list(inspect.signature(strategy.choose_move).parameters),
            ["turn", "my_history", "opponent_history", "rng"],
        )

    def test_seeded_strategy_is_deterministic_and_emits_only_legal_moves(self) -> None:
        first_rng = random.Random(8675309)
        second_rng = random.Random(8675309)
        first = [strategy.choose_move(1, "", "", first_rng) for _ in range(12)]
        second = [strategy.choose_move(1, "", "", second_rng) for _ in range(12)]

        self.assertEqual(first, second)
        self.assertLessEqual(set(first), {"R", "P", "S"})


if __name__ == "__main__":
    unittest.main()
