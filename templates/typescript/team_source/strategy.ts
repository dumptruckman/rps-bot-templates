export function chooseMove(
  turn: number,
  myHistory: string,
  opponentHistory: string,
  rng: { nextInt(upperExclusive: number): number }
): string {
  const moves = ["R", "P", "S"];
  return moves[rng.nextInt(moves.length)];
}
