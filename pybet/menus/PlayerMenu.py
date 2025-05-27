from typing import Optional
from pybet.models.PlayerManager import PlayerManager
from pybet.models.DataPersistence import DataPersistence
from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult

DATA_FILE: str = './pybet/data/players.json'

def manage_players() -> None:
    """
    Menu for managing player operations: list, add, update, delete.
    """
    manager: PlayerManager = PlayerManager(DATA_FILE)

    while True:
        print("\n--- Manage Players ---")
        print("1. List all players")
        print("2. Add a new player")
        print("3. Update a player")
        print("4. Delete a player")
        print("0. Back to main menu")
        sub: str = input("Choose an action: ").strip()

        if sub == '1':
            res: OperationResult = manager.get_all_players()
            if not res.ok:
                print("Error:", res.error)
            else:
                players: list[Player] = res.data
                if not players:
                    print("No players found.")
                else:
                    print("\nPlayers:")
                    for p in players:
                        print(f"- ID: {p.id} | Name: {p.name} | Balance: {p.account_balance}")

        elif sub == '2':
            name: str = input("Enter full name: ").strip()
            bal_str: str = input("Enter initial balance: ").strip()
            try:
                balance: float = float(bal_str)
                res: OperationResult = manager.add_player(name, balance)
                if res.ok:
                    p: Player = res.data
                    print(f"Player created: ID {p.id}, Name {p.name}, Balance {p.account_balance}")
                else:
                    print("Error:", res.error)
            except ValueError:
                print("Invalid balance.")

        elif sub == '3':
            pid: str = input("Enter player ID to update: ").strip()
            new_name: Optional[str] = input("New name (leave blank to keep current): ").strip()
            if new_name == "":
                new_name = None
            new_bal_str: str = input("New balance (leave blank to keep current): ").strip()
            new_balance: Optional[float] = None
            if new_bal_str:
                try:
                    new_balance = float(new_bal_str)
                except ValueError:
                    print("Invalid balance. Aborting update.")
                    continue
            res: OperationResult = manager.update_player(pid, new_name, new_balance)
            if res.ok:
                p: Player = res.data
                print(f"Updated player: ID {p.id}, Name {p.name}, Balance {p.account_balance}")
            else:
                print("Error:", res.error)

        elif sub == '4':
            pid: str = input("Enter player ID to delete: ").strip()
            res: OperationResult = manager.delete_player(pid)
            if res.ok:
                p: Player = res.data
                print(f"Deleted player: ID {p.id}, Name {p.name}")
            else:
                print("Error:", res.error)

        elif sub == '0':
            break
        else:
            print("Invalid option, try again.")
