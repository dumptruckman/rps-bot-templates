import java.util.random.RandomGenerator;

public final class Strategy {
    private Strategy() {}

    /** Returns one legal move using only the wrapper-provided random stream. */
    public static String chooseMove(
        int turn,
        String myHistory,
        String opponentHistory,
        RandomGenerator rng
    ) {
        String[] moves = {"R", "P", "S"};
        return moves[rng.nextInt(moves.length)];
    }
}
