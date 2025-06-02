from typing import List
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.models.OperationResult import OperationResult

def view_history() -> None:
    """
    Menu to interact with a specific player's history.
    """
    while True:
        player_id = input("Enter Player ID (or 0 to back): ").strip()
        if player_id == '0':
            return
        hist = PlayerHistory(player_id)
        get_res = hist.get_all()
        if not get_res.ok:
            print("Error:", get_res.error)
            continue

        while True:
            print(f"\n--- History for {player_id} ---")
            print("1. Show all actions")
            print("2. Push new action")
            print("3. Pop last action")
            print("0. Back to player select")
            choice = input("Choose: ").strip()

            if choice == '1':
                actions: List[str] = get_res.data
                if not actions:
                    print("No history.")
                else:
                    for i, a in enumerate(actions, 1):
                        print(f"{i}. {a}")

            elif choice == '2':
                action = input("Enter action description: ").strip()
                if action:
                    res = hist.push(action)
                    print("OK." if res.ok else "Error: "+res.error)
                get_res = hist.get_all()

            elif choice == '3':
                res = hist.pop()
                if res.ok:
                    print("Popped:", res.data)
                else:
                    print("Error:", res.error)
                get_res = hist.get_all()

            elif choice == '0':
                break
            else:
                print("Invalid.")