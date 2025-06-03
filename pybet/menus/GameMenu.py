from rich.console import Console
from rich.text import Text

from pybet.models.PlayerManager import PlayerManager
from pybet.games.slot_game import play_slot
from pybet.games.guessing_game import play_guessing

console = Console()

def play_games() -> None:
    """
    Displays a menu for the user to choose between two games:
        1) Tragamonedas (Slot Machine)
        2) Adivinanzas (Guessing Game)

    Each game now implements:
      - Tragamonedas: brute‐force combination generation
      - Adivinanzas: tail recursion to compute optimal attempts
    """
    manager = PlayerManager()

    while True:
        console.print("\n[bold cyan]--- Jugar ---[/bold cyan]")
        console.print("1. Tragamonedas")
        console.print("2. Adivinanzas")
        console.print("0. Volver al menú principal")
        choice: str = console.input("[yellow]Seleccione un juego:[/yellow] ").strip()

        if choice == '1':
            play_slot(manager)
        elif choice == '2':
            play_guessing(manager)
        elif choice == '0':
            break
        else:
            console.print("[red]Opción inválida, intente de nuevo.[/red]")