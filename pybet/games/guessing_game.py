"""
Guessing game module for the PyBet application.

This module implements the guessing game logic and user interface.

Guessing Game (“Adivinanzas”) module with tail recursion to compute optimal attempts.

This version first computes, via a tail‐recursive function, 
the minimum worst‐case number of guesses needed to find a secret number
in a given range [1..N]. Then it lets the user play once.

Steps:
1. Prompt for player ID → verify existence and load current balance.
2. Prompt for bet amount → validate > 0 and ≤ balance.
3. Prompt for range limit N (e.g., “¿Hasta qué número quieres jugar?”).
    -- Compute optimal worst‐case attempts using tail recursion.
    -- Display that “You will need at most X attempts (worst case).”
4. Generate a random “secret” integer ∈ [1..N].
5. Let the user guess up to X times; for each:
    - If guess == secret → award = 4×bet, break and win.
    - If guess ≠ secret and attempts remain → inform higher or lower.
6. If user did not guess in X attempts → they lose the bet.
7. Update balance accordingly, record a descriptive string in PlayerHistory, display result.

Docstring tags:
    - Manager: PlayerManager instance
    - OperationResult: for reading/updating JSON
    - PlayerHistory: to push a descriptive string
"""

import random
from typing import Optional, Tuple

from rich.console import Console
from rich.text import Text

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory

# Add this import to enable earning history tracking
from pybet.helpers.EarningsTracker import EarningsTracker

console = Console()

def tail_recursive_optimal(low: int, high: int, attempts: int = 0) -> int:
    """
    Tail‐recursive helper to compute the minimum number of worst‐case guesses needed
    to find any secret in the interval [low..high], assuming an optimal binary-search strategy.

    Returns:
        int: Minimum worst‐case number of attempts.
    """
    # Base case: if interval size is 1, only one attempt needed
    size = high - low + 1
    if size <= 1:
        return attempts + 1

    # Choose pivot as the middle guess: mid = (low + high) // 2
    mid = (low + high) // 2

    # Splitting into two subintervals: [low..mid-1] and [mid+1..high]
    # Worst‐case size is the larger half
    left_size = mid - 1 - low + 1
    right_size = high - (mid + 1) + 1

    # Determine which side is larger, and recurse on that side
    if left_size >= right_size:
        # Worst‐case secret lies in left side
        return tail_recursive_optimal(low, mid - 1, attempts + 1)
    else:
        # Worst‐case secret lies in right side
        return tail_recursive_optimal(mid + 1, high, attempts + 1)


def play_guessing(manager: PlayerManager) -> None:
    """
    Simulates a “Adivinanzas” (Guessing Game) with tail recursion for optimal attempts.

    Procedure:
        1. Prompt for player ID → verify existence and get current balance.
        2. Prompt for bet amount → validate > 0 and ≤ balance.
        3. Prompt for “range limit” N (integer ≥ 2).
            - Compute minimum worst‐case attempts via tail‐recursive function.
            - Display to user: “In the worst case, you need X attempts to guess a number from 1 to N.”
        4. Generate a random secret ∈ [1..N].
        5. Loop up to X times:
            a. Prompt “Guess a number (1–N):”
            b. If guess == secret → reward = 4×bet; break & won.
            c. If guess < secret → print “Más alto.”
            If guess > secret → print “Más bajo.”
        6. If user never guessed in X attempts → they lose (reward = –bet).
        7. Update player balance and record one descriptive string in PlayerHistory:
            e.g. “Adivinanzas: Range=1–N, bet=B, secret=S, outcome=won/lost, balance=…”
        8. Print final result.

    Args:
        manager (PlayerManager): Instance to load/update players.json.
    """
    console.print("[bold cyan]=== Adivinanzas (Guessing Game) ===[/bold cyan]")
    player_id = console.input("[yellow]ID de jugador:[/yellow] ").strip()
    get_res: OperationResult = manager.get_player_by_id(player_id)
    if not get_res.ok:
        console.print(f"[red]Error:[/] {get_res.error}")
        return

    player = get_res.data  # type: ignore  # Player instance

    bet_str = console.input("[yellow]Monto a apostar:[/yellow] ").strip()
    try:
        bet: float = float(bet_str)
    except ValueError:
        console.print("[red]Apuesta inválida. Debe ser un número.[/red]")
        return

    if bet <= 0:
        console.print("[red]La apuesta debe ser mayor que cero.[/red]")
        return

    if bet > player.account_balance:
        console.print("[red]Saldo insuficiente para esa apuesta.[/red]")
        return

    # —— Determine the numeric range for guessing —— 
    n_str = console.input("[yellow]¿Hasta qué número quieres jugar? (Ingrese entero ≥ 2):[/yellow] ").strip()
    try:
        N: int = int(n_str)
    except ValueError:
        console.print("[red]Número inválido. Debe ser un entero.[/red]")
        return

    if N < 2:
        console.print("[red]El número debe ser al menos 2.[/red]")
        return

    # Compute, via tail recursion, the minimum worst‐case attempts
    optimal_attempts = tail_recursive_optimal(1, N, 0)
    console.print(f"[green]En el peor de los casos, necesitas {optimal_attempts} intentos para adivinar un número entre 1 y {N}.[/green]\n")

    # —— Generate the secret number _______
    secret = random.randint(1, N)

    # —— Let the player guess up to optimal_attempts times —— 
    guess_count = 0
    won = False
    while guess_count < optimal_attempts:
        guess_str = console.input(f"[yellow]Adivina el número (intento {guess_count + 1}/{optimal_attempts}):[/yellow] ").strip()
        try:
            guess = int(guess_str)
        except ValueError:
            console.print("[red]Número inválido. Debe ser un entero entre 1 y[/] [cyan]" + str(N) + "[/cyan]")
            continue

        if guess < 1 or guess > N:
            console.print(f"[red]Número fuera de rango. Debe ser entre 1 y {N}.[/red]")
            continue

        guess_count += 1
        if guess == secret:
            # Player wins: payout is 4× bet
            reward = bet * 4
            new_balance = player.account_balance + reward
            console.print(f"[bold green]¡Correcto! Ganaste {reward:.2f}.[/bold green]")
            won = True
            break
        else:
            if guess < secret:
                console.print("[yellow]Más alto.[/yellow]")
            else:
                console.print("[yellow]Más bajo.[/yellow]")

    # If did not win after all attempts → lose bet
    if not won:
        reward = -bet
        new_balance = player.account_balance + reward
        console.print(f"[bold red]Lo siento, no lo adivinaste. Perdiste {bet:.2f}. El número era {secret}.[/bold red]")

    # Build a descriptive history entry
    if won:
        outcome_str = f"adivinó {secret}, ganó {reward}, saldo {new_balance}"
    else:
        outcome_str = f"falló (salió {secret}), perdió {bet}, saldo {new_balance}"

    result_str = f"Adivinanzas: Rango 1–{N}, apostó {bet}, {outcome_str}"

    # Update the player’s balance in JSON
    upd_res: OperationResult = manager.update_player(player_id, None, new_balance)
    if not upd_res.ok:
        console.print(f"[red]Error al actualizar balance:[/] {upd_res.error}")
        return

    # Record in player's history
    hist = PlayerHistory(player_id)
    push_res: OperationResult = hist.push(result_str)
    if not push_res.ok:
        console.print(f"[red]Error al registrar historial:[/] {push_res.error}")

    # to update earnings history
    EarningsTracker.update_earnings(player_id, reward)

    console.print("\n[bold cyan]Resultado Adivinanzas:[/bold cyan]")
    console.print(f"{result_str}")