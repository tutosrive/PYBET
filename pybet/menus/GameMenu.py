from typing import Optional
import random

from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory

def play_games() -> None:
    """
    Presenta un menú para que el usuario elija entre dos juegos:
        1) Tragamonedas
        2) Adivinanzas

    Para cada juego:
        - Se solicita ID de jugador y monto de apuesta.
        - Se valida que el jugador exista y tenga saldo suficiente.
        - Se simula un resultado sencillo (para registrar histórico y actualizar saldo).
        - Se actualiza el balance en players.json mediante PlayerManager.
        - Se registra la jugada en PlayerHistory.
        - Se muestra el resultado en pantalla.
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
    Simula una jugada sencilla de “Tragamonedas”:
        - Pide ID de jugador y monto de apuesta.
        - Verifica existencia y saldo.
        - Gana el jugador con probabilidad 50%: recupera apuesta + premio igual a apuesta.
        - En caso contrario, pierde la apuesta.
        - Actualiza saldo y registra historial con PlayerHistory.
    """
    player_id = input("ID de jugador: ").strip()
    # Verificar que exista
    get_p = manager.get_player_by_id(player_id)
    if not get_p.ok:
        print("Error:", get_p.error)
        return

    player = get_p.data  # instancia Player
    # Pedir monto de apuesta
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

    # Simular resultado 50/50
    win = random.choice([True, False])
    if win:
        # Gana: se le acredita apuesta de vuelta + ganancia
        reward = bet  # premio igual a la apuesta
        new_balance = player.account_balance + reward
        result_str = f"Tragamonedas: Apostó {bet}, ganó {reward}, saldo {new_balance}"
    else:
        # Pierde: resta apuesta
        new_balance = player.account_balance - bet
        result_str = f"Tragamonedas: Apostó {bet}, perdió {bet}, saldo {new_balance}"

    # Actualizar dato en JSON
    upd_res: OperationResult = manager.update_player(player_id, None, new_balance)
    if not upd_res.ok:
        print("Error al actualizar balance:", upd_res.error)
        return

    # Registrar en historial individual
    hist = PlayerHistory(player_id)
    push_res = hist.push(result_str)
    if not push_res.ok:
        print("Error al registrar historial:", push_res.error)

    print("\nResultado Tragamonedas:")
    print(result_str)


def _play_guessing(manager: PlayerManager) -> None:
    """
    Simula una jugada sencilla de “Adivinanzas”:
        - Pide ID de jugador y monto de apuesta.
        - Verifica existencia y saldo.
        - Genera un número aleatorio entre 1 y 5. El jugador adivina.
        - Si acierta, gana 4× apuesta; si falla, pierde la apuesta.
        - Actualiza saldo y registra historial con PlayerHistory.
    """
    player_id = input("ID de jugador: ").strip()
    get_p = manager.get_player_by_id(player_id)
    if not get_p.ok:
        print("Error:", get_p.error)
        return

    player = get_p.data
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

    # Jugada de adivinanzas: elegir número del 1 al 5
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
        # Premio: 4× la apuesta
        reward = bet * 4
        new_balance = player.account_balance + reward
        result_str = (f"Adivinanzas: Apostó {bet}, adivinó {secret}, ganó {reward}, saldo {new_balance}")
    else:
        # Pierde: quita apuesta
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