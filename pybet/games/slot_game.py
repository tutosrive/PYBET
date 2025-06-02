"""
Slot Machine (“Tragamonedas”) module.

This version uses a brute-force approach to generate every possible
combination of symbols across three reels and decide which are winning.
All combinations are generated via three nested loops (no itertools).

Steps:
1. Define a fixed set of symbols for each of the three reels.
2. Brute-force generate all 3-symbol combinations using nested loops.
3. Mark any combination where all three symbols match as a winning combo.
4. When the user plays, spin by randomly choosing one symbol per reel.
5. Check—via membership in the precomputed “winning” set—whether the spin wins.
6. If win, reward = bet; else, reward = –bet. Update the player’s balance and history.

Dependencies:
    - random: for spinning each reel
    - PlayerManager: to load/update player data in JSON
    - OperationResult: to handle success/failure of updates
    - PlayerHistory: to record a descriptive string for each play

All code is pure Python standard library.
"""

import random
from typing import List, Tuple

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory

# Define the possible symbols for each reel
REEL_SYMBOLS: List[str] = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]

# Brute-force generation of all possible 3-symbol combinations (nested loops)
ALL_COMBINATIONS: List[Tuple[str, str, str]] = []
for s1 in REEL_SYMBOLS:
    for s2 in REEL_SYMBOLS:
        for s3 in REEL_SYMBOLS:
            ALL_COMBINATIONS.append((s1, s2, s3))

# Define the winning combinations: any triple where all three symbols match
WINNING_COMBINATIONS = {
    combo for combo in ALL_COMBINATIONS if combo[0] == combo[1] == combo[2]
}


def play_slot(manager: PlayerManager) -> None:
    """
    Simulates a “Tragamonedas” (Slot Machine) play with brute-force-backed logic.

    Procedure:
        1. Prompt for player ID → verify existence and load current balance.
        2. Prompt for bet amount → validate > 0 and ≤ balance.
        3. “Spin” by randomly choosing one symbol per reel.
        4. Check if (symbol1, symbol2, symbol3) is in WINNING_COMBINATIONS.
        5. If win: reward = bet; else: reward = -bet.
        6. Update the player’s balance via PlayerManager.
        7. Record a descriptive string in PlayerHistory.
        8. Display spin result and updated balance.

    Args:
        manager (PlayerManager): Instance to load/update players.json.
    """
    player_id = input("ID de jugador: ").strip()
    get_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_res.ok:
        print("Error:", get_res.error)
        return

    player = get_res.data  # type: ignore  # Player instance

    bet_str = input("Monto a apostar: ").strip()
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

    # —— Spin the three reels (random choice per reel) ——
    spin_result = (
        random.choice(REEL_SYMBOLS),
        random.choice(REEL_SYMBOLS),
        random.choice(REEL_SYMBOLS),
    )

    # Determine win or loss via membership in WINNING_COMBINATIONS
    if spin_result in WINNING_COMBINATIONS:
        reward = bet
        new_balance = player.account_balance + reward
        win_str = f"won {reward}"
    else:
        reward = -bet
        new_balance = player.account_balance + reward
        win_str = f"lost {bet}"

    # Build descriptive string for history
    reel_display = " | ".join(spin_result)
    result_str = (
        f"Tragamonedas: Spin [{reel_display}] → {win_str.upper()}, "
        f"new balance {new_balance}"
    )

    # Update balance in JSON
    upd_res: OperationResult = manager.update_player(player_id, None, new_balance)
    if not upd_res.ok:
        print("Error al actualizar balance:", upd_res.error)
        return

    # Record the play in player's history
    hist = PlayerHistory(player_id)
    push_res: OperationResult = hist.push(result_str)
    if not push_res.ok:
        print("Error al registrar historial:", push_res.error)

    # Display result to user
    print("\nResultado Tragamonedas:")
    print(result_str)