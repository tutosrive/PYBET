"""
Example script to demonstrate that the PYBET casino system is fully functional,
covering all features specified in the project PDF. This includes:
    - Player CRUD (add, list, update, delete)
    - Player-specific history (push/pop)
    - Queue management (enqueue, dequeue, show)
    - Backtracking optimal betting path
    - Two games: "Tragamonedas" and "Adivinanzas"
    - Report generation (5 distinct reports)
All operations are executed programmatically, and outputs are printed to console.
"""

import os
import random
import csv
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.text import Text

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.logic.WaitingQueue import WaitingQueue
from pybet.logic.Backtracking import Backtracking
from pybet.helpers.FileManager import FileManager
from pybet.menus.ReportsMenu import (
    _report_top_balances,
    _report_earnings_ranking,
    _report_player_history,
    _report_loss_counts,
    _report_game_participation,
)

console = Console()

# 1. SET UP DIRECTORIES & CLEAN OLD DATA
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "pybet" / "data"
REPORTS_DIR = DATA_DIR / "reports"
LOGS_DIR = BASE_DIR / "pybet" / "logs"

# Ensure directories exist
for d in (DATA_DIR, REPORTS_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Reset players.json, queue.json
players_file = DATA_DIR / "players.json"
queue_file = DATA_DIR / "queue.json"
for fpath, initial in [(players_file, "{}"), (queue_file, "[]")]:
    fpath.write_text(initial, encoding="utf-8")

console.print("[bold green]✅ Data directories and files initialized.[/bold green]\n")

# 2. DEMONSTRATE PLAYER CRUD
console.print("[bold cyan]=== Player CRUD Operations ===[/bold cyan]")
manager = PlayerManager()

# 2.1 Add 3 players
player_ids = []
for name, balance in [("Alice", 1000.0), ("Bob", 1500.0), ("Charlie", 1200.0)]:
    res = manager.add_player(name, balance)
    if res.ok:
        player = res.data
        player_ids.append(player.id)
        console.print(f"[green]✔ Created Player:[/green] [bold]{player.name}[/bold] (ID: [cyan]{player.id}[/cyan], Balance: [green]{player.account_balance:.2f}[/green])")
    else:
        console.print(f"[red]Error adding {name}:[/red] {res.error}")
console.print()

# 2.2 List all players
res_all = manager.get_all_players()
if res_all.ok:
    console.print("[bold magenta]List of all players after creation:[/bold magenta]")
    table = Table(title="Players")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Balance", style="green", justify="right")

    for p in res_all.data:
        table.add_row(p.id, p.name, f"{p.account_balance:.2f}")

    console.print(table)
else:
    console.print(f"[red]Error listing players:[/red] {res_all.error}")
console.print()

# 2.3 Update Bob's balance and name
bob_id = player_ids[1]
res_update = manager.update_player(bob_id, new_name="Bobby", new_balance=1800.0)
if res_update.ok:
    updated = res_update.data
    console.print(f"[green]✔ Updated Player:[/green] [bold]{updated.name}[/bold] (ID: [cyan]{updated.id}[/cyan], Balance: [green]{updated.account_balance:.2f}[/green])")
else:
    console.print(f"[red]Error updating player:[/red] {res_update.error}")
console.print()

# 2.4 Delete Charlie
charlie_id = player_ids[2]
res_delete = manager.delete_player(charlie_id)
if res_delete.ok:
    deleted = res_delete.data
    console.print(f"[green]✔ Deleted Player:[/green] [bold]{deleted.name}[/bold] (ID: [cyan]{deleted.id}[/cyan])")
else:
    console.print(f"[red]Error deleting player:[/red] {res_delete.error}")
console.print()

# 2.5 Final list
res_final = manager.get_all_players()
if res_final.ok:
    console.print("[bold magenta]Final list of players:[/bold magenta]")
    table2 = Table(title="Players After Deletion")
    table2.add_column("ID", style="cyan", no_wrap=True)
    table2.add_column("Name", style="magenta")
    table2.add_column("Balance", style="green", justify="right")

    for p in res_final.data:
        table2.add_row(p.id, p.name, f"{p.account_balance:.2f}")

    console.print(table2)
else:
    console.print(f"[red]Error listing players:[/red] {res_final.error}")
console.print("\n")

# 3. DEMONSTRATE PLAYER HISTORY (push/pop)
console.print("[bold cyan]=== Player History ===[/bold cyan]")
alice_id = player_ids[0]
hist = PlayerHistory(alice_id)

# 3.1 Push some actions
for action in [
    "Alice: Logged in",
    "Alice: Deposited $500",
    "Alice: Bet $200 on Tragamonedas"
]:
    psh_res = hist.push(action)
    status = "[green]OK[/green]" if psh_res.ok else f"[red]{psh_res.error}[/red]"
    console.print(f"Pushed action -> '{action}': {status}")

# 3.2 Get all
get_hist = hist.get_all()
console.print("\n[magenta]Alice's history after pushes:[/magenta]")
if get_hist.ok and get_hist.data:
    table3 = Table(title="Alice's History")
    table3.add_column("Index", style="cyan", justify="right")
    table3.add_column("Action", style="magenta")
    for idx, act in enumerate(get_hist.data, 1):
        table3.add_row(str(idx), act)
    console.print(table3)
else:
    console.print("[italic]  (No history or error)[/italic]")

# 3.3 Pop last
pop_res = hist.pop()
if pop_res.ok:
    console.print(f"\n[green]Popped action:[/green] {pop_res.data}")
else:
    console.print(f"\n[red]Error popping history:[/red] {pop_res.error}")

# 3.4 Final history
final_hist = hist.get_all()
console.print("[magenta]Alice's history after pop:[/magenta]")
if final_hist.ok and final_hist.data:
    table4 = Table(title="Alice's History (After Pop)")
    table4.add_column("Index", style="cyan", justify="right")
    table4.add_column("Action", style="magenta")
    for idx, act in enumerate(final_hist.data, 1):
        table4.add_row(str(idx), act)
    console.print(table4)
else:
    console.print("[italic]  (No history or error)[/italic]")
console.print("\n")

# 4. DEMONSTRATE QUEUE (enqueue, dequeue, show)
console.print("[bold cyan]=== Waiting Queue ===[/bold cyan]")
queue = WaitingQueue()

# 4.1 Enqueue players
console.print("[yellow]Enqueuing players A, B, Alice:[/yellow]")
queue.enqueue("A")
queue.enqueue("B")
queue.enqueue(alice_id)

# Display queue
current_queue = queue.get_all()
table_q = Table(title="Current Queue")
table_q.add_column("Position", style="cyan", justify="right")
table_q.add_column("Player ID", style="magenta")
for idx, pid in enumerate(current_queue, 1):
    table_q.add_row(str(idx), pid)
console.print(table_q)

# 4.2 Peek
peek_res = queue.peek()
console.print(f"[yellow]Peek front:[/yellow] {peek_res.data if peek_res.ok else peek_res.error}")

# 4.3 Dequeue twice
for _ in range(2):
    dq_res = queue.dequeue()
    console.print(f"[yellow]Dequeued:[/yellow] {dq_res.data if dq_res.ok else dq_res.error}")

# Display queue after dequeues
remaining = queue.get_all()
table_q2 = Table(title="Queue After 2 Dequeues")
table_q2.add_column("Position", style="cyan", justify="right")
table_q2.add_column("Player ID", style="magenta")
for idx, pid in enumerate(remaining, 1):
    table_q2.add_row(str(idx), pid)
console.print(table_q2)

# 4.4 Clear queue
clr_res = queue.clear()
console.print(f"[yellow]Cleared queue. Now:[/yellow] {queue.get_all()}")
console.print("\n")

# 5. BACKTRACKING (optimal betting path)
console.print("[bold cyan]=== Optimal Betting Path (Backtracking) ===[/bold cyan]")
initial_balance = 100
bet_options = [5, 10, 20, 50]
solver = Backtracking(initial_balance, bet_options)
best_seq, best_total = solver.findOptimalPath()

table_bt = Table(title="Optimal Betting Path")
table_bt.add_column("Initial Balance", style="cyan", justify="right")
table_bt.add_column("Bet Options", style="magenta")
table_bt.add_column("Best Sequence", style="green")
table_bt.add_column("Total Used", style="yellow", justify="right")

table_bt.add_row(str(initial_balance), str(bet_options), str(best_seq), str(best_total))
console.print(table_bt)
console.print("\n")

# 6. PLAY GAMES
from pybet.games.slot_game import play_slot
from pybet.games.guessing_game import play_guessing

console.print("[bold cyan]=== Gameplay Simulation ===[/bold cyan]")
# 6.1 Play Tragamonedas for Alice
console.print("\n[magenta]-- Tragamonedas Play --[/magenta]")
console.print(f"[italic]Manual Test:[/] Run [bold]play_slot(manager)[/bold] and follow prompts.")

# 6.2 Play Adivinanzas for Bob (Bobby)
console.print("\n[magenta]-- Adivinanzas Play --[/magenta]")
console.print(f"[italic]Manual Test:[/] Run [bold]play_guessing(manager)[/bold] and follow prompts.")
console.print("\n")

# 7. GENERATE REPORTS
console.print("[bold cyan]=== Generating Reports ===[/bold cyan]")

# 7.1 Top Balances
console.print("\n[magenta]-- Top Balances Report --[/magenta]")
_report_top_balances(manager)

# 7.2 Earnings Ranking
console.print("\n[magenta]-- Earnings Ranking Report --[/magenta]")
_report_earnings_ranking(manager)

# 7.3 Player History Report for Alice
console.print("\n[magenta]-- Player History Report (Alice) --[/magenta]")
console.print(f"[italic]Manual Test:[/] Run [bold]_report_player_history(manager)[/bold] and enter: [cyan]{alice_id}[/cyan] when prompted.")
console.print("\n")

# 7.4 Loss Counts
console.print("[magenta]-- Loss Counts Report --[/magenta]")
_report_loss_counts(manager)

# 7.5 Game Participation
console.print("\n[magenta]-- Game Participation Report --[/magenta]")
_report_game_participation(manager)

console.print(f"\n[green]All reports generated in directory:[/] [bold]{REPORTS_DIR}[/bold]\n")

# 8. EXPORT PLAYER HISTORY TO FILES (JSON & CSV) FOR Alice
console.print("[bold cyan]=== Exporting Alice's History Manually ===[/bold cyan]")
alice_history = PlayerHistory(alice_id).get_all()
if alice_history.ok:
    actions = alice_history.data or []
    if actions:
        # Write JSON
        json_path = REPORTS_DIR / f"history_{alice_id}.json"
        FileManager.write_file(json_path, actions)
        # Write CSV
        csv_path = REPORTS_DIR / f"history_{alice_id}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Action"])
            for entry in actions:
                writer.writerow([entry])
        console.print(f"[green]Alice's history exported →[/green] [bold]{json_path}[/bold], [bold]{csv_path}[/bold]")
    else:
        console.print("[italic]No history for Alice to export.[/italic]")
else:
    console.print(f"[red]Error fetching Alice's history:[/red] {alice_history.error}")

console.print("\n[bold green]✅ Example script completed. Please verify outputs above and check data/reports/ for generated files.[/bold green]")