from rich.console import Console
from rich.table import Table

from typing import List
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.models.OperationResult import OperationResult

console = Console()

def view_history() -> None:
    """
    Menu to interact with a specific player's history.
    """
    while True:
        player_id = console.input("[yellow]Ingrese ID de jugador (o 0 para volver):[/yellow] ").strip()
        if player_id == '0':
            return

        hist = PlayerHistory(player_id)
        get_res: OperationResult = hist.get_all()
        if not get_res.ok:
            console.print(f"[red]Error:[/red] {get_res.error}")
            continue

        while True:
            console.print(f"\n[bold cyan]--- Historial de {player_id} ---[/bold cyan]")
            console.print("1. Mostrar todas las acciones")
            console.print("2. Agregar nueva acción")
            console.print("3. Eliminar última acción")
            console.print("0. Volver a selección de jugador")
            choice = console.input("[yellow]Seleccione:[/yellow] ").strip()

            if choice == '1':
                actions: List[str] = get_res.data
                if not actions:
                    console.print("[italic]Sin historial.[/italic]")
                else:
                    table = Table(title=f"Historial de {player_id}")
                    table.add_column("N.º", style="cyan", justify="right")
                    table.add_column("Acción", style="magenta")
                    for i, a in enumerate(actions, 1):
                        table.add_row(str(i), a)
                    console.print(table)

            elif choice == '2':
                action = console.input("[yellow]Ingrese descripción de la acción:[/yellow] ").strip()
                if action:
                    res = hist.push(action)
                    if res.ok:
                        console.print("[green]✔ Acción registrada.[/green]")
                    else:
                        console.print(f"[red]Error:[/red] {res.error}")
                get_res = hist.get_all()

            elif choice == '3':
                res = hist.pop()
                if res.ok:
                    console.print(f"[green]✔ Eliminado:[/green] {res.data}")
                else:
                    console.print(f"[red]Error:[/red] {res.error}")
                get_res = hist.get_all()

            elif choice == '0':
                break
            else:
                console.print("[red]Opción inválida.[/red]")