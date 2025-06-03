from typing import List, Dict
from pathlib import Path
import csv

from rich.console import Console
from rich.table import Table

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.models.Player import Player
from pybet.helpers.FileManager import FileManager

console = Console()
DATA_FILE: str = './pybet/data/players.json'
REPORTS_DIR: str = './pybet/data/reports'

def generate_reports() -> None:
    """
    Menu to generate various player/game reports,
    exporting each both to JSON and CSV, mostrando tablas.
    """
    manager: PlayerManager = PlayerManager()
    # Ensure reports directory exists
    Path(REPORTS_DIR).mkdir(parents=True, exist_ok=True)

    while True:
        console.print("\n[bold cyan]--- Generar Reportes ---[/bold cyan]")
        console.print("1. Top Balances")
        console.print("2. Earnings Ranking")
        console.print("3. Historial de Jugador (por jugador)")
        console.print("4. Ranking de Pérdidas")
        console.print("5. Participación por Juego")
        console.print("0. Volver al menú principal")
        choice: str = console.input("[yellow]Seleccione un reporte:[/yellow] ").strip()

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
            console.print("[red]Opción inválida, intente de nuevo.[/red]")


# Report 1: Top Balances
def _report_top_balances(manager: PlayerManager) -> None:
    """
    Gathers all players, sorts them by account_balance descending,
    muestra tabla en pantalla y exporta a JSON+CSV.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        console.print(f"[red]Error cargando jugadores:[/red] {res.error}")
        return

    players: List[Player] = res.data
    # Sort descending by balance
    sorted_players = sorted(players, key=lambda p: p.account_balance, reverse=True)

    # Prepare display and export data (Show table)
    table = Table(title="Top Balances")
    table.add_column("Posición", style="cyan", justify="right")
    table.add_column("Nombre", style="magenta")
    table.add_column("Saldo", style="green", justify="right")

    json_data = []
    csv_rows: List[List[str]] = []
    for rank, p in enumerate(sorted_players, 1):
        table.add_row(str(rank), p.name, f"{p.account_balance:.2f}")
        json_data.append({"rank": rank, "name": p.name, "balance": p.account_balance})
        csv_rows.append([str(rank), p.name, f"{p.account_balance:.2f}"])

    console.print(table)

    # Paths for JSON and CSV files
    json_path = f"{REPORTS_DIR}/top_balances.json"
    csv_path = f"{REPORTS_DIR}/top_balances.csv"
    # Write JSON
    FileManager.write_file(json_path, json_data, mode='w')
    # Write CSV
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Rank","Name","Balance"], mode='w')
    console.print(f"[green]→ Guardado en[/green] [bold]{json_path}[/bold] [green]y[/green] [bold]{csv_path}[/bold]")


# Report 2: Earnings Ranking
def _report_earnings_ranking(manager: PlayerManager) -> None:
    """
    Similar to Top Balances pero incluye ranking numérico.
    Muestra tabla y exporta a JSON+CSV.
    """
    res = manager.get_all_players()
    if not res.ok:
        console.print(f"[red]Error cargando jugadores:[/red] {res.error}")
        return

    players = res.data
    # Sort descending by balance
    sorted_players = sorted(players, key=lambda p: p.account_balance, reverse=True)

    table = Table(title="Ranking de Ganancias")
    table.add_column("Posición", style="cyan", justify="right")
    table.add_column("Nombre", style="magenta")
    table.add_column("Saldo", style="green", justify="right")

    json_data = []
    csv_rows: List[List[str]] = []
    for rank, p in enumerate(sorted_players, 1):
        table.add_row(str(rank), p.name, f"{p.account_balance:.2f}")
        json_data.append({"rank": rank, "name": p.name, "balance": p.account_balance})
        csv_rows.append([str(rank), p.name, f"{p.account_balance:.2f}"])

    console.print(table)

    # Paths for JSON and CSV files
    json_path = f"{REPORTS_DIR}/earnings_ranking.json"
    csv_path = f"{REPORTS_DIR}/earnings_ranking.csv"
    FileManager.write_file(json_path, json_data, mode='w')
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Rank","Name","Balance"], mode='w')
    console.print(f"[green]→ Guardado en[/green] [bold]{json_path}[/bold] [green]y[/green] [bold]{csv_path}[/bold]")


# Report 3: Player History
def _report_player_history(manager: PlayerManager) -> None:
    """
    Prompts for un ID de jugador, obtiene su historial via PlayerHistory,
    muestra en tabla y exporta a JSON+CSV.
    """
    player_id = console.input("[yellow]Ingrese el ID del jugador (o 0 para cancelar):[/yellow] ").strip()
    if player_id == '0':
        return

    # Verify the player exists
    get_player_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_player_res.ok:
        console.print(f"[red]Error:[/red] {get_player_res.error}")
        return

    hist = PlayerHistory(player_id)
    get_hist_res: OperationResult = hist.get_all()
    if not get_hist_res.ok:
        console.print(f"[red]Error obteniendo historial:[/red] {get_hist_res.error}")
        return

    actions: List[str] = get_hist_res.data
    if not actions:
        console.print("[italic]El jugador no tiene historial.[/italic]")
    else:
        table = Table(title=f"Historial de {player_id}")
        table.add_column("N.º", style="cyan", justify="right")
        table.add_column("Acción", style="magenta")
        for idx, action in enumerate(actions, 1):
            table.add_row(str(idx), action)
        console.print(table)

    # Export to JSON and CSV
    json_path = f"{REPORTS_DIR}/history_{player_id}.json"
    csv_path = f"{REPORTS_DIR}/history_{player_id}.csv"

    # JSON format: list of strings
    FileManager.write_file(json_path, actions, mode='w')
    # CSV format: single column "Action"
    FileManager.write_file_csv(csv_path, rows=[[a] for a in actions], header=["Action"], mode='w')
    console.print(f"[green]→ Historial exportado en[/green] [bold]{json_path}[/bold] [green]y[/green] [bold]{csv_path}[/bold]")


# Report 4: Loss Counts
def _report_loss_counts(manager: PlayerManager) -> None:
    """
    Calcula cuántas veces cada jugador ha perdido,
    muestra tabla y exporta a JSON+CSV.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        console.print(f"[red]Error cargando jugadores:[/red] {res.error}")
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

    table = Table(title="Ranking de Pérdidas")
    table.add_column("Posición", style="cyan", justify="right")
    table.add_column("Nombre", style="magenta")
    table.add_column("Cant. Pérdidas", style="red", justify="right")
    for idx, entry in enumerate(sorted_losses, 1):
        table.add_row(str(idx), entry["name"], str(entry["loss_count"]))
    console.print(table)

    # Export JSON and CSV
    json_path = f"{REPORTS_DIR}/loss_counts.json"
    csv_path = f"{REPORTS_DIR}/loss_counts.csv"
    FileManager.write_file(json_path, sorted_losses, mode='w')

    # CSV header: ["Rank", "Name", "LossCount"]
    csv_rows: List[List[str]] = []
    for rank, entry in enumerate(sorted_losses, 1):
        csv_rows.append([str(rank), entry["name"], str(entry["loss_count"])])
    FileManager.write_file_csv(csv_path, rows=csv_rows, header=["Rank", "Name", "LossCount"], mode='w')
    console.print(f"[green]→ Guardado en[/green] [bold]{json_path}[/bold] [green]y[/green] [bold]{csv_path}[/bold]")


# Report 5: Game Participation
def _report_game_participation(manager: PlayerManager) -> None:
    """
    Cuenta cuántas jugadas de “Tragamonedas” vs “Adivinanzas” hay en todos los historiales,
    muestra tabla y exporta a JSON+CSV.
    """
    res: OperationResult = manager.get_all_players()
    if not res.ok:
        console.print(f"[red]Error cargando jugadores:[/red] {res.error}")
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

    table = Table(title="Participación por Juego")
    table.add_column("Juego", style="cyan")
    table.add_column("Cantidad", style="magenta", justify="right")
    table.add_row("Tragamonedas", str(trag_count))
    table.add_row("Adivinanzas", str(adivin_count))
    console.print(table)

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
    console.print(f"[green]→ Guardado en[/green] [bold]{json_path}[/bold] [green]y[/green] [bold]{csv_path}[/bold]")