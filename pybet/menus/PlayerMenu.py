"""
Player management menu for the PyBet application.

This module provides the interface for managing players, including adding, removing, and listing players in the system.
"""

from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.text import Text

from pybet.models.PlayerManager import PlayerManager
from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult

console = Console()

def manage_players() -> None:
    """
    Menu for managing player operations: list, add, update, delete.
    Uses PlayerManager, which stores all players in players.json.
    """
    manager = PlayerManager()

    while True:
        console.print("\n[bold cyan]--- Gestionar Jugadores ---[/bold cyan]")
        console.print("1. Listar todos los jugadores")
        console.print("2. Agregar nuevo jugador")
        console.print("3. Actualizar jugador")
        console.print("4. Eliminar jugador")
        console.print("0. Volver al menú principal")
        sub: str = console.input("[yellow]Seleccione una opción:[/yellow] ").strip()

        if sub == '1':
            res: OperationResult = manager.get_all_players()
            if not res.ok:
                console.print(f"[red]Error:[/red] {res.error}")
            else:
                players: list[Player] = res.data
                if not players:
                    console.print("[italic]No hay jugadores.[/italic]")
                else:
                    # Construct table with Rich
                    table = Table(title="Jugadores Registrados")
                    table.add_column("ID", style="cyan", no_wrap=True)
                    table.add_column("Nombre", style="magenta")
                    table.add_column("Saldo", style="green", justify="right")
                    table.add_column("Creado en", style="dim")

                    for p in players:
                        table.add_row(p.id, p.name, f"{p.account_balance:.2f}", p.created_at)

                    console.print(table)

        elif sub == '2':
            name: str = console.input("[yellow]Ingrese nombre completo:[/yellow] ").strip()
            bal_str: str = console.input("[yellow]Ingrese saldo inicial:[/yellow] ").strip()
            try:
                balance: float = float(bal_str)
                res: OperationResult = manager.add_player(name, balance)
                if res.ok:
                    p: Player = res.data
                    console.print(f"[green]✔ Jugador creado:[/green] ID [bold]{p.id}[/bold], Nombre [bold]{p.name}[/bold], Saldo [bold]{p.account_balance:.2f}[/bold]")
                else:
                    console.print(f"[red]Error:[/red] {res.error}")
            except ValueError:
                console.print("[red]Saldo inválido. Debe ser un número.[/red]")

        elif sub == '3':
            pid: str = console.input("[yellow]Ingrese ID de jugador a actualizar:[/yellow] ").strip()
            new_name: Optional[str] = console.input("[yellow]Nuevo nombre (dejar vacío para conservar):[/yellow] ").strip()
            if new_name == "":
                new_name = None
            new_bal_str: str = console.input("[yellow]Nuevo saldo (dejar vacío para conservar):[/yellow] ").strip()
            new_balance: Optional[float] = None
            if new_bal_str:
                try:
                    new_balance = float(new_bal_str)
                except ValueError:
                    console.print("[red]Saldo inválido. Abortando actualización.[/red]")
                    continue
            res: OperationResult = manager.update_player(pid, new_name, new_balance)
            if res.ok:
                p: Player = res.data
                console.print(f"[green]✔ Jugador actualizado:[/green] ID [bold]{p.id}[/bold], Nombre [bold]{p.name}[/bold], Saldo [bold]{p.account_balance:.2f}[/bold]")
            else:
                console.print(f"[red]Error:[/red] {res.error}")

        elif sub == '4':
            pid: str = console.input("[yellow]Ingrese ID de jugador a eliminar:[/yellow] ").strip()
            res: OperationResult = manager.delete_player(pid)
            if res.ok:
                p: Player = res.data
                console.print(f"[green]✔ Jugador eliminado:[/green] ID [bold]{p.id}[/bold], Nombre [bold]{p.name}[/bold]")
            else:
                console.print(f"[red]Error:[/red] {res.error}")

        elif sub == '0':
            break
        else:
            console.print("[red]Opción inválida, intente de nuevo.[/red]")