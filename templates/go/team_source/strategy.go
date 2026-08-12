package main

import rand "math/rand/v2"

// ChooseMove returns one legal move using only the wrapper-provided random stream.
func ChooseMove(turn int, myHistory, opponentHistory string, rng *rand.Rand) string {
	moves := [...]string{"R", "P", "S"}
	return moves[rng.IntN(len(moves))]
}
