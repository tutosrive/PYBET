from typing import List
from rich.console import Console
from rich.table import Table

from pybet.logic.Backtracking import Backtracking
from pybet.models.OperationResult import OperationResult

console = Console()

def optimal_betting_path() -> None:
    """
    Menu to compute the optimal betting path (subset-sum) for a given balance
    and list of bet options.
    """
    while True:
        console.print("\n[bold cyan]--- Camino Óptimo de Apuestas ---[/bold cyan]")
        console.print("1. Calcular apuestas óptimas")
        console.print("0. Volver al menú principal")
        choice: str = console.input("[yellow]Seleccione una opción:[/yellow] ").strip()

        if choice == '1':
            bal_str: str = console.input("[yellow]Ingrese saldo inicial (entero):[/yellow] ").strip()
            try:
                initial_balance: int = int(bal_str)
            except ValueError:
                console.print("[red]Saldo inválido. Debe ser un número entero.[/red]")
                continue

            opts_str: str = console.input(
                "[yellow]Ingrese opciones de apuesta separadas por coma (ej. 5,10,20):[/yellow] "
            ).strip()
            try:
                bet_options: List[int] = [
                    int(x.strip()) for x in opts_str.split(',') if x.strip()
                ]
            except ValueError:
                console.print("[red]Opciones inválidas. Asegúrese de ingresar números enteros separados por coma.[/red]")
                continue

            solver = Backtracking(initial_balance, bet_options)
            best_seq, best_total = solver.findOptimalPath()

            table = Table(title="Resultado de Apuesta Óptima")
            table.add_column("Saldo Inicial", justify="center", style="cyan")
            table.add_column("Opciones", justify="center", style="magenta")
            table.add_column("Secuencia Óptima", justify="center", style="green")
            table.add_column("Total Apostado", justify="center", style="yellow")

            table.add_row(
                str(initial_balance),
                str(bet_options),
                str(best_seq),
                str(best_total)
            )

            console.print(table)

        elif choice == '0':
            break
        else:
            console.print("[red]Opción inválida, intente de nuevo.[/red]")