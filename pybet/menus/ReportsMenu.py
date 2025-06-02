from typing import List, Dict
from pathlib import Path
import csv

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.models.Player import Player
from pybet.helpers.FileManager import FileManager

DATA_FILE: str = './pybet/data/players.json'
REPORTS_DIR: str = './pybet/data/reports'

def generate_reports() -> None:
    """
    Menu to generate various player/game reports,
    exporting each both to JSON and CSV.
    """
    manager: PlayerManager = PlayerManager()
    # Ensure reports directory exists
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)

    while True:
        print("\n--- Generar Reportes ---")
        print("1. Top Balances")
        print("2. Earnings Ranking")
        print("3. Historial de Jugador (por jugador)")
        print("4. Ranking de Pérdidas")
        print("5. Participación por Juego")
        print("0. Volver al menú principal")
        choice: str = input("Seleccione un reporte: ").strip()

        if choice == '1':
            _report_top_balances(manager)
        elif choice == '2':
            _report_earnings_ranking(manager)
        elif choice == '3':
            _report_player_history(manager)
        elif choice == '4':
            _report_loss_counts(manager)
        elif choice == '5':
            _report_game_participation(manager)
        elif choice == '0':
            break
        else:
            print("Opción inválida, intente de nuevo.")


# Report 1: Top Balances
def _report_top_balances(manager: PlayerManager) -> None:
    """
    Gathers all players, sorts them by account_balance descending,
    displays on screen and exports to JSON+CSV.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        print("Error cargando jugadores:", res.error)
        return

    players: List[Player] = res.data
    # Sort descending by balance
    sorted_players = sorted(players, key=lambda p: p.account_balance, reverse=True)

    # Prepare display and export data
    print("\nTop Balances:")
    json_data = []
    csv_rows: List[List[str]] = []
    for p in sorted_players:
        print(f"- {p.name}: ${p.account_balance}")
        json_data.append({"name": p.name, "balance": p.account_balance})
        csv_rows.append([p.name, str(p.account_balance)])

    # Paths for JSON and CSV files
    json_path = f"{REPORTS_DIR}/top_balances.json"
    csv_path = f"{REPORTS_DIR}/top_balances.csv"

    # Write JSON
    FileManager.write_file(json_path, json_data, mode='w')
    # Write CSV
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Name", "Balance"], mode='w')

    print(f"→ Guardado en {json_path} y {csv_path}")


# Report 2: Earnings Ranking
def _report_earnings_ranking(manager: PlayerManager) -> None:
    """
    Similar to Top Balances but includes ranking position.
    Exports to JSON+CSV.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        print("Error cargando jugadores:", res.error)
        return

    players: List[Player] = res.data
    # Sort descending by balance
    sorted_players = sorted(players, key=lambda p: p.account_balance, reverse=True)

    print("\nRanking de Ganancias:")
    json_data = []
    csv_rows: List[List[str]] = []
    for rank, p in enumerate(sorted_players, 1):
        print(f"{rank}. {p.name} — ${p.account_balance}")
        json_data.append({"rank": rank, "name": p.name, "balance": p.account_balance})
        csv_rows.append([str(rank), p.name, str(p.account_balance)])

    # Paths for JSON and CSV files
    json_path = f"{REPORTS_DIR}/earnings_ranking.json"
    csv_path = f"{REPORTS_DIR}/earnings_ranking.csv"

    FileManager.write_file(json_path, json_data, mode='w')
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Rank", "Name", "Balance"], mode='w')

    print(f"→ Guardado en {json_path} y {csv_path}")


# Report 3: Player History
def _report_player_history(manager: PlayerManager) -> None:
    """
    Prompts for a player ID, retrieves that player's history via PlayerHistory,
    displays on screen and exports to JSON+CSV.
    """
    player_id = input("Ingrese el ID del jugador (o 0 para cancelar): ").strip()
    if player_id == '0':
        return

    # Verify the player exists
    get_player_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_player_res.ok:
        print("Error:", get_player_res.error)
        return

    hist = PlayerHistory(player_id)
    get_hist_res: OperationResult = hist.get_all()
    if not get_hist_res.ok:
        print("Error obteniendo historial:", get_hist_res.error)
        return

    actions: List[str] = get_hist_res.data
    if not actions:
        print("El jugador no tiene historial.")
    else:
        print(f"\nHistorial de Jugador {player_id}:")
        for idx, action in enumerate(actions, 1):
            print(f"{idx}. {action}")

    # Export to JSON and CSV
    json_path = f"{REPORTS_DIR}/history_{player_id}.json"
    csv_path = f"{REPORTS_DIR}/history_{player_id}.csv"

    # JSON format: list of strings
    FileManager.write_file(json_path, actions, mode='w')
    # CSV format: single column "Action"
    FileManager.write_file_csv(csv_path, rows=[[a] for a in actions], header=["Action"], mode='w')

    print(f"→ Historico exportado en {json_path} y {csv_path}")


# Report 4: Loss Counts
def _report_loss_counts(manager: PlayerManager) -> None:
    """
    Computes, for each player, how many times their history contains “perdió” or “perdio”
    (case-insensitive). Sorts descending by that count, displays and exports.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        print("Error cargando jugadores:", res.error)
        return

    players: List[Player] = res.data
    loss_list: List[Dict[str, int]] = []

    for p in players:
        # Count occurrences of "lost" in their history
        count = 0
        for action in p.history:
            low = action.lower()
            if "perdió" in low or "perdio" in low:
                count += 1
        loss_list.append({"name": p.name, "loss_count": count})

    # Sort descending by loss_count
    sorted_losses = sorted(loss_list, key=lambda x: x["loss_count"], reverse=True)

    print("\nRanking de Pérdidas:")
    for idx, entry in enumerate(sorted_losses, 1):
        print(f"{idx}. {entry['name']} — {entry['loss_count']} pérdidas")

    # Export JSON and CSV
    json_path = f"{REPORTS_DIR}/loss_counts.json"
    csv_path = f"{REPORTS_DIR}/loss_counts.csv"

    FileManager.write_file(json_path, sorted_losses, mode='w')

    # CSV header: ["Rank", "Name", "LossCount"]
    csv_rows: List[List[str]] = []
    for rank, entry in enumerate(sorted_losses, 1):
        csv_rows.append([str(rank), entry["name"], str(entry["loss_count"])])
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Rank", "Name", "LossCount"], mode='w')

    print(f"→ Guardado en {json_path} y {csv_path}")


# Report 5: Game Participation
def _report_game_participation(manager: PlayerManager) -> None:
    """
    Counts how many times “Tragamonedas” vs “Adivinanzas” appear across all players' histories.
    Displays and exports the totals.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        print("Error cargando jugadores:", res.error)
        return

    players: List[Player] = res.data
    trag_count = 0
    adivin_count = 0

    for p in players:
        for action in p.history:
            low = action.lower()
            if "tragamonedas" in low:
                trag_count += 1
            if "adivinanzas" in low:
                adivin_count += 1

    print("\nParticipación por Juego:")
    print(f"- Tragamonedas: {trag_count} jugadas")
    print(f"- Adivinanzas: {adivin_count} jugadas")

    # Export JSON and CSV
    json_data = [
        {"game": "Tragamonedas", "count": trag_count},
        {"game": "Adivinanzas", "count": adivin_count},
    ]
    json_path = f"{REPORTS_DIR}/game_participation.json"
    FileManager.write_file(json_path, json_data, mode='w')

    csv_rows: List[List[str]] = [
        ["Tragamonedas", str(trag_count)],
        ["Adivinanzas", str(adivin_count)]
    ]
    csv_path = f"{REPORTS_DIR}/game_participation.csv"
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Game", "Count"], mode='w')

    print(f"→ Guardado en {json_path} y {csv_path}")