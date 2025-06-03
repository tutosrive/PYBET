from rich.console import Console
from rich.table import Table

from pybet.logic.WaitingQueue import WaitingQueue
from pybet.models.OperationResult import OperationResult

console = Console()
queue: WaitingQueue = WaitingQueue()

def manage_queue() -> None:
    """
    Manages the waiting queue: enqueue, dequeue, and display contents.
    """
    while True:
        console.print("\n[bold cyan]--- Manejar Cola de Espera ---[/bold cyan]")
        console.print("1. Encolar jugador")
        console.print("2. Desencolar jugador")
        console.print("3. Mostrar cola")
        console.print("0. Volver al menú principal")
        option: str = console.input("[yellow]Seleccione una opción:[/yellow] ").strip()

        if option == '1':
            player_id: str = console.input("[yellow]Ingrese ID de jugador para encolar:[/yellow] ").strip()
            if player_id:
                queue.enqueue(player_id)
                console.print(f"[green]✔ Jugador {player_id} agregado a la cola.[/green]")
            else:
                console.print("[red]El ID de jugador no puede estar vacío.[/red]")

        elif option == '2':
            result: OperationResult = queue.dequeue()
            if result.ok:
                console.print(f"[green]✔ Jugador {result.data} removido de la cola.[/green]")
            else:
                console.print("[red]La cola está vacía.[/red]")

        elif option == '3':
            current: list[str] = queue.get_all()
            if not current:
                console.print("[italic]La cola está vacía.[/italic]")
            else:
                table = Table(title="Cola de Espera")
                table.add_column("Posición", style="cyan", justify="right")
                table.add_column("ID de Jugador", style="magenta")
                for i, pid in enumerate(current, 1):
                    table.add_row(str(i), pid)
                console.print(table)

        elif option == '0':
            break
        else:
            console.print("[red]Opción inválida.[/red]")