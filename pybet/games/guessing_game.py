from typing import Optional
import random
from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory

def play_guessing(manager: PlayerManager) -> None:
    """
    Simulates a “Adivinanzas” (Guessing) play:
        - Prompts for player ID and bet amount.
        - Verifies player existence and sufficient balance.
        - Generates a random number between 1 and 5; player must guess.
        - If guessed correctly, player wins 4× bet; otherwise loses the bet.
        - Updates the player’s balance in players.json via PlayerManager.
        - Records the play in the player’s history via PlayerHistory.
        - Displays the result on screen.

    Args:
        manager (PlayerManager): Instance of PlayerManager to load/update players.
    """
    player_id: str = input("ID de jugador: ").strip()
    get_player_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_player_res.ok:
        print("Error:", get_player_res.error)
        return

    player = get_player_res.data  # type: ignore  # Instancia Player
    bet_str: str = input("Monto a apostar: ").strip()
    try:
        bet: float = float(bet_str)
    except ValueError:
        print("Apuesta inválida. Debe ser un número.")
        return

    if bet <= 0:
        print("La apuesta debe ser mayor que cero.")
        return

    if bet > player.account_balance:
        print("Saldo insuficiente para esa apuesta.")
        return

    # Generate secret number 1–5
    secret: int = random.randint(1, 5)
    guess_str: str = input("Adivina el número (1-5): ").strip()
    try:
        guess: int = int(guess_str)
    except ValueError:
        print("Número inválido. Debe ser un entero entre 1 y 5.")
        return

    if guess < 1 or guess > 5:
        print("Número fuera de rango. Debe ser entre 1 y 5.")
        return

    if guess == secret:
        reward: float = bet * 4
        new_balance: float = player.account_balance + reward
        result_str: str = (
            f"Adivinanzas: Apostó {bet}, adivinó {secret}, ganó {reward}, saldo {new_balance}"
        )
    else:
        new_balance = player.account_balance - bet
        result_str = (
            f"Adivinanzas: Apostó {bet}, falló (salió {secret}), perdió {bet}, saldo {new_balance}"
        )

    # Update balance in JSON
    upd_res: OperationResult = manager.update_player(player_id, None, new_balance)
    if not upd_res.ok:
        print("Error al actualizar balance:", upd_res.error)
        return

    # Record in player's history
    hist = PlayerHistory(player_id)
    push_res: OperationResult = hist.push(result_str)
    if not push_res.ok:
        print("Error al registrar historial:", push_res.error)

    print("\nResultado Adivinanzas:")
    print(result_str)