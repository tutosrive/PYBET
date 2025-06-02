from pybet.models.PlayerManager import PlayerManager
from pybet.games.slot_game import play_slot
from pybet.games.guessing_game import play_guessing

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
        print("\n--- Jugar ---")
        print("1. Tragamonedas")
        print("2. Adivinanzas")
        print("0. Volver al menú principal")
        choice: str = input("Seleccione un juego: ").strip()

        if choice == '1':
            play_slot(manager)
        elif choice == '2':
            play_guessing(manager)
        elif choice == '0':
            break
        else:
            print("Opción inválida, intente de nuevo.")