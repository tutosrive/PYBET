from typing import Optional
import random
from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory

def play_slot(manager: PlayerManager) -> None:
    """
    Simulates a “Tragamonedas” (Slot Machine) play:
        - Prompts for player ID and bet amount.
        - Verifies player existence and sufficient balance.
        - With 50% chance, player wins: returns the bet plus a prize equal to the bet.
            Otherwise, loses the bet.
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

    # Simulate 50/50 result
    win: bool = random.choice([True, False])
    if win:
        reward: float = bet  # Premio igual a la apuesta
        new_balance: float = player.account_balance + reward
        result_str: str = f"Tragamonedas: Apostó {bet}, ganó {reward}, saldo {new_balance}"
    else:
        new_balance = player.account_balance - bet
        result_str = f"Tragamonedas: Apostó {bet}, perdió {bet}, saldo {new_balance}"

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

    print("\nResultado Tragamonedas:")
    print(result_str)