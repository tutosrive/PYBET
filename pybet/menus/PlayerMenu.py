from typing import Optional
from pybet.models.PlayerManager import PlayerManager
from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult

def manage_players() -> None:
    """
    Menu for managing player operations: list, add, update, delete.
    Uses PlayerManager, which stores all players in players.json.
    """
    manager = PlayerManager()

    while True:
        print("\n--- Gestionar Jugadores ---")
        print("1. Listar todos los jugadores")
        print("2. Agregar nuevo jugador")
        print("3. Actualizar jugador")
        print("4. Eliminar jugador")
        print("0. Volver al menú principal")
        sub: str = input("Seleccione una opción: ").strip()

        if sub == '1':
            res: OperationResult = manager.get_all_players()
            if not res.ok:
                print("Error:", res.error)
            else:
                players: list[Player] = res.data
                if not players:
                    print("No hay jugadores.")
                else:
                    print("\nJugadores:")
                    for p in players:
                        print(f"- ID: {p.id} | Nombre: {p.name} | Saldo: {p.account_balance}")

        elif sub == '2':
            name: str = input("Ingrese nombre completo: ").strip()
            bal_str: str = input("Ingrese saldo inicial: ").strip()
            try:
                balance: float = float(bal_str)
                res: OperationResult = manager.add_player(name, balance)
                if res.ok:
                    p: Player = res.data
                    print(f"Jugador creado: ID {p.id}, Nombre {p.name}, Saldo {p.account_balance}")
                else:
                    print("Error:", res.error)
            except ValueError:
                print("Saldo inválido. Debe ser un número.")

        elif sub == '3':
            pid: str = input("Ingrese ID de jugador a actualizar: ").strip()
            new_name: Optional[str] = input("Nuevo nombre (dejar vacío para conservar): ").strip()
            if new_name == "":
                new_name = None
            new_bal_str: str = input("Nuevo saldo (dejar vacío para conservar): ").strip()
            new_balance: Optional[float] = None
            if new_bal_str:
                try:
                    new_balance = float(new_bal_str)
                except ValueError:
                    print("Saldo inválido. Abortando actualización.")
                    continue
            res: OperationResult = manager.update_player(pid, new_name, new_balance)
            if res.ok:
                p: Player = res.data
                print(f"Jugador actualizado: ID {p.id}, Nombre {p.name}, Saldo {p.account_balance}")
            else:
                print("Error:", res.error)

        elif sub == '4':
            pid: str = input("Ingrese ID de jugador a eliminar: ").strip()
            res: OperationResult = manager.delete_player(pid)
            if res.ok:
                p: Player = res.data
                print(f"Jugador eliminado: ID {p.id}, Nombre {p.name}")
            else:
                print("Error:", res.error)

        elif sub == '0':
            break
        else:
            print("Opción inválida, intente de nuevo.")