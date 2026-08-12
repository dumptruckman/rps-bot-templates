package main

import (
	rand "math/rand/v2"
	"testing"
)

func seeded(seed uint64) *rand.Rand {
	return rand.New(rand.NewPCG(seed, seed+1))
}

func TestChooseMoveReturnsOnlyLegalMoves(t *testing.T) {
	rng := seeded(42)
	for turn := 1; turn <= 100; turn++ {
		move := ChooseMove(turn, "", "", rng)
		if move != "R" && move != "P" && move != "S" {
			t.Fatalf("turn %d returned illegal move %q", turn, move)
		}
	}
}

func TestChooseMoveIsDeterministicForTheBotVisibleSeed(t *testing.T) {
	first := seeded(18446744073709551615)
	second := seeded(18446744073709551615)
	for turn := 1; turn <= 100; turn++ {
		moveA := ChooseMove(turn, "R", "P", first)
		moveB := ChooseMove(turn, "R", "P", second)
		if moveA != moveB {
			t.Fatalf("turn %d differed for the same seed: %q != %q", turn, moveA, moveB)
		}
	}
}
