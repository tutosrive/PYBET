from typing import List
from pybet.logic.Backtracking import Backtracking
from pybet.models.OperationResult import OperationResult

def optimal_betting_path() -> None:
    """
    Menu to compute the optimal betting path (subset-sum) for a given balance
    and list of bet options.
    """
    while True:
        print("\n--- Optimal Betting Path ---")
        print("1. Compute optimal bets")
        print("0. Back to main menu")
        choice: str = input("Choose an action: ").strip()

        if choice == '1':
            bal_str: str = input("Enter initial balance (integer): ").strip()
            try:
                initial_balance: int = int(bal_str)
            except ValueError:
                print("Invalid balance. Please enter an integer.")
                continue

            opts_str: str = input(
                "Enter bet options as comma-separated integers (e.g. 5,10,20): "
            ).strip()
            try:
                bet_options: List[int] = [
                    int(x.strip()) for x in opts_str.split(',') if x.strip()
                ]
            except ValueError:
                print("Invalid bet options. Ensure all are integers.")
                continue

            solver = Backtracking(initial_balance, bet_options)
            best_seq, best_total = solver.findOptimalPath()
            print(f"\nInitial balance: {initial_balance}")
            print(f"Bet options: {bet_options}")
            print(f"Optimal sequence of bets: {best_seq}")
            print(f"Total amount used: {best_total}")

        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")