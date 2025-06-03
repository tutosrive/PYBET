from rich.console import Console
from rich.table import Table
from rich.text import Text

from pybet.menus.PlayerMenu import manage_players
from pybet.menus.GameMenu import play_games
from pybet.menus.HistoryMenu import view_history
from pybet.menus.QueueMenu import manage_queue
from pybet.menus.BacktrackingMenu import optimal_betting_path
from pybet.menus.ReportsMenu import generate_reports

console = Console()

def main():
    while True:
        console.print("\n[bold cyan]=== Menú Principal ===[/bold cyan]")
        console.print("1. Gestionar Jugadores")
        console.print("2. Jugar")
        console.print("3. Ver Historial")
        console.print("4. Manejar Cola de Espera")
        console.print("5. Camino Óptimo de Apuestas")
        console.print("6. Generar Reportes")
        console.print("0. Salir")

        choice = console.input("[yellow]Seleccione una opción:[/yellow] ").strip()

        if choice == '1':
            manage_players()
        elif choice == '2':
            play_games()
        elif choice == '3':
            view_history()
        elif choice == '4':
            manage_queue()
        elif choice == '5':
            optimal_betting_path()
        elif choice == '6':
            generate_reports()
        elif choice == '0':
            console.print("[bold green]¡Hasta luego![/bold green]")
            break
        else:
            console.print("[red]Opción inválida, intente de nuevo.[/red]")

if __name__ == '__main__':
    main()