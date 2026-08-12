import java.util.SplittableRandom;

public final class StrategyTest {
    private StrategyTest() {}

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void chooseMoveReturnsOnlyLegalMoves() {
        var rng = new SplittableRandom(42L);
        for (int turn = 1; turn <= 100; turn++) {
            String move = Strategy.chooseMove(turn, "", "", rng);
            require(
                move.equals("R") || move.equals("P") || move.equals("S"),
                "turn " + turn + " returned illegal move " + move
            );
        }
    }

    private static void chooseMoveIsDeterministicForTheBotVisibleSeed() {
        long seed = Long.parseUnsignedLong("18446744073709551615");
        var first = new SplittableRandom(seed);
        var second = new SplittableRandom(seed);
        for (int turn = 1; turn <= 100; turn++) {
            String moveA = Strategy.chooseMove(turn, "R", "P", first);
            String moveB = Strategy.chooseMove(turn, "R", "P", second);
            require(
                moveA.equals(moveB),
                "turn " + turn + " differed for the same bot-visible seed"
            );
        }
    }

    public static void main(String[] arguments) {
        chooseMoveReturnsOnlyLegalMoves();
        chooseMoveIsDeterministicForTheBotVisibleSeed();
    }
}
