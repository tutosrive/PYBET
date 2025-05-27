from typing import List
from pathlib import Path

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.Algorithms import Algorithms
from pybet.models.Player import Player
from pybet.helpers.FileManager import FileManager

DATA_FILE: str = './pybet/data/players.json'
REPORTS_DIR: str = './pybet/data/reports'

def generate_reports() -> None:
    """
    Menu to generate various player/game reports,
    exporting each both to JSON and CSV.
    """
    manager: PlayerManager = PlayerManager(DATA_FILE)
    # Ensure reports directory exists
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)

    while True:
        print("\n--- Generate Reports ---")
        print("1. Top Balances")
        print("2. Earnings Ranking")
        print("3. Player History (per player)") 
        print("4. Loss Counts")
        print("5. Game Participation")
        print("0. Back to main menu")
        choice: str = input("Select a report: ").strip()

        if choice == '1':
            # Top Balances
            res: OperationResult = manager.get_all_players()
            if not res.ok:
                print("Error loading players:", res.error)
            else:
                players: List[Player] = res.data
                # Sort descending by balance
                sorted_players = sorted(players, key=lambda p: p.account_balance, reverse=True)

                # Prepare display and export data
                print("\nTop Balances:")
                json_data = []
                csv_rows = []
                for p in sorted_players:
                    print(f"- {p.name}: ${p.account_balance}")
                    json_data.append({"name": p.name, "balance": p.account_balance})
                    csv_rows.append([p.name, str(p.account_balance)])

                # Paths
                json_path = f"{REPORTS_DIR}/top_balances.json"
                csv_path  = f"{REPORTS_DIR}/top_balances.csv"

                # Write JSON
                FileManager.write_file(json_path, json_data, mode='w')
                # Write CSV
                FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Name", "Balance"], mode='w')

                print(f"→ Saved to {json_path} and {csv_path}")

        elif choice == '2':
            # Earnings Ranking (same as top balances for now)
            res = manager.get_all_players()
            if not res.ok:
                print("Error loading players:", res.error)
            else:
                players = res.data
                sorted_players = sorted(players, key=lambda p: p.account_balance, reverse=True)

                print("\nEarnings Ranking:")
                json_data = []
                csv_rows = []
                for rank, p in enumerate(sorted_players, 1):
                    print(f"{rank}. {p.name} — ${p.account_balance}")
                    json_data.append({"rank": rank, "name": p.name, "balance": p.account_balance})
                    csv_rows.append([str(rank), p.name, str(p.account_balance)])

                json_path = f"{REPORTS_DIR}/earnings_ranking.json"
                csv_path  = f"{REPORTS_DIR}/earnings_ranking.csv"

                FileManager.write_file(json_path, json_data, mode='w')
                FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Rank","Name","Balance"], mode='w')

                print(f"→ Saved to {json_path} and {csv_path}")

        elif choice == '3':
            print("Player History report not yet implemented.")
        elif choice == '4':
            print("Loss Counts report not yet implemented.")
        elif choice == '5':
            print("Game Participation report not yet implemented.")
        elif choice == '0':
            break
        else:
            print("Invalid option, try again.")
