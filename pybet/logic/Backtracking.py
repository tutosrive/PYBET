class Backtracking:
    """
    Encapsulates the logic to find the optimal sequence of bets (subset‐sum)
    that maximizes total wagered without exceeding the initial balance.
    """

    def __init__(self, initialBalance: int, betOptions: list[int]) -> None:
        """
        Initializes the backtracking solver.

        Args:
            initialBalance (int): The total funds available.
            betOptions (list[int]): list of distinct bet amounts.
        """
        self.initialBalance: int = initialBalance
        self.betOptions: list[int] = betOptions
        self.bestSequence: list[int] = []
        self.bestTotal: int = 0

    def findOptimalPath(self) -> tuple[list[int], int]:
        """
        Executes the backtracking search.

        Returns:
            tuple[list[int], int]:
                - list of bet amounts chosen.
                - Sum of those bets.
        """
        # Start the recursion
        self._backtrack(0, [], 0)
        return self.bestSequence, self.bestTotal

    def _backtrack(self, startIndex: int, currentSeq: list[int], currentSum: int) -> None:
        """
        Recursively builds sequences of bets.

        Args:
            startIndex (int): Next index in betOptions to consider.
            currentSeq (list[int]): Sequence built so far.
            currentSum (int): Sum of currentSeq.
        """
        # Update best if we have a better total
        if currentSum > self.bestTotal:
            self.bestTotal = currentSum
            self.bestSequence = currentSeq.copy()

        # Try adding each remaining bet
        for idx in range(startIndex, len(self.betOptions)):
            nextBet = self.betOptions[idx]
            newSum = currentSum + nextBet

            # Prune paths that exceed the balance
            if newSum > self.initialBalance:
                continue

            currentSeq.append(nextBet)
            self._backtrack(idx + 1, currentSeq, newSum)
            currentSeq.pop()
