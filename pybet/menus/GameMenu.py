from typing import Optional
import random

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory

def play_games() -> None:
    """
    Displays a menu for the user to choose between two games:
        1) Tragamonedas
        2) Adivinanzas

    For each game:
        - Prompts for player ID and bet amount.
        - Validates that the player exists and has sufficient balance.
        - Simulates a simple outcome (to record in history and update balance).
        - Updates the player's balance via PlayerManager.
        - Logs the play in PlayerHistory.
        - Shows the result on screen.
    """
    manager = PlayerManager()

    while True:
        print("\n--- Jugar ---")
        print("1. Tragamonedas")
        print("2. Adivinanzas")
        print("0. Volver al menú principal")
        choice: str = input("Seleccione un juego: ").strip()

        if choice == '1':
            _play_slots(manager)
        elif choice == '2':
            _play_guessing(manager)
        elif choice == '0':
            break
        else:
            print("Opción inválida, intente de nuevo.")


def _play_slots(manager: PlayerManager) -> None:
    """
    Simulates a simple “Slots” play:
        - Requests player ID and bet amount.
        - Verifies existence and balance.
        - 50% chance to win: returns bet plus a prize equal to bet.
        - Otherwise loses the bet.
        - Updates balance and registers history with PlayerHistory.
    """
    player_id = input("ID de jugador: ").strip()
    get_player_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_player_res.ok:
        print("Error:", get_player_res.error)
        return

    player = get_player_res.data  # instance of Player
    bet_str = input("Monto a apostar: ").strip()
    try:
        bet = float(bet_str)
    except ValueError:
        print("Apuesta inválida. Debe ser un número.")
        return

    if bet <= 0:
        print("La apuesta debe ser mayor que cero.")
        return

    if bet > player.account_balance:
        print("Saldo insuficiente para esa apuesta.")
        return

    # Simulate 50/50 result
    win = random.choice([True, False])
    if win:
        reward = bet  # prize equal to bet
        new_balance = player.account_balance + reward
        result_str = f"Tragamonedas: Apostó {bet}, ganó {reward}, saldo {new_balance}"
    else:
        new_balance = player.account_balance - bet
        result_str = f"Tragamonedas: Apostó {bet}, perdió {bet}, saldo {new_balance}"

    # Update balance in JSON
    upd_res: OperationResult = manager.update_player(player_id, None, new_balance)
    if not upd_res.ok:
        print("Error al actualizar balance:", upd_res.error)
        return

    # Log in player's history
    hist = PlayerHistory(player_id)
    push_res = hist.push(result_str)
    if not push_res.ok:
        print("Error al registrar historial:", push_res.error)

    print("\nResultado Tragamonedas:")
    print(result_str)


def _play_guessing(manager: PlayerManager) -> None:
    """
    Simulates a simple “Guessing” game:
        - Requests player ID and bet amount.
        - Verifies existence and balance.
        - Generates a random number 1–5; player guesses.
        - If correct, wins 4× bet; if wrong, loses the bet.
        - Updates balance and registers history with PlayerHistory.
    """
    player_id = input("ID de jugador: ").strip()
    get_player_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_player_res.ok:
        print("Error:", get_player_res.error)
        return

    player = get_player_res.data
    bet_str = input("Monto a apostar: ").strip()
    try:
        bet = float(bet_str)
    except ValueError:
        print("Apuesta inválida. Debe ser un número.")
        return

    if bet <= 0:
        print("La apuesta debe ser mayor que cero.")
        return

    if bet > player.account_balance:
        print("Saldo insuficiente para esa apuesta.")
        return

    # Generate number between 1 and 5
    secret = random.randint(1, 5)
    guess_str = input("Adivina el número (1-5): ").strip()
    try:
        guess = int(guess_str)
    except ValueError:
        print("Número inválido. Debe ser un entero entre 1 y 5.")
        return

    if guess < 1 or guess > 5:
        print("Número fuera de rango. Debe ser entre 1 y 5.")
        return

    if guess == secret:
        # Win: 4x the bet
        reward = bet * 4
        new_balance = player.account_balance + reward
        result_str = (f"Adivinanzas: Apostó {bet}, adivinó {secret}, ganó {reward}, saldo {new_balance}")
    else:
        # Lost: Quit the bet
        new_balance = player.account_balance - bet
        result_str = (f"Adivinanzas: Apostó {bet}, falló (salió {secret}), perdió {bet}, saldo {new_balance}")

    upd_res: OperationResult = manager.update_player(player_id, None, new_balance)
    if not upd_res.ok:
        print("Error al actualizar balance:", upd_res.error)
        return

    hist = PlayerHistory(player_id)
    push_res = hist.push(result_str)
    if not push_res.ok:
        print("Error al registrar historial:", push_res.error)

    print("\nResultado Adivinanzas:")
    print(result_str)