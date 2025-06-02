from typing import List
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.models.OperationResult import OperationResult

def view_history() -> None:
    """
    Menu to interact with a specific player's history.
    """
    while True:
        player_id = input("Ingrese ID de jugador (o 0 para volver): ").strip()
        if player_id == '0':
            return

        hist = PlayerHistory(player_id)
        get_res: OperationResult = hist.get_all()
        if not get_res.ok:
            print("Error:", get_res.error)
            continue

        while True:
            print(f"\n--- Historial de {player_id} ---")
            print("1. Mostrar todas las acciones")
            print("2. Agregar nueva acción")
            print("3. Eliminar última acción")
            print("0. Volver a selección de jugador")
            choice = input("Seleccione: ").strip()

            if choice == '1':
                actions: List[str] = get_res.data
                if not actions:
                    print("Sin historial.")
                else:
                    for i, a in enumerate(actions, 1):
                        print(f"{i}. {a}")

            elif choice == '2':
                action = input("Ingrese descripción de la acción: ").strip()
                if action:
                    res = hist.push(action)
                    print("OK." if res.ok else "Error: " + res.error)
                get_res = hist.get_all()

            elif choice == '3':
                res = hist.pop()
                if res.ok:
                    print("Eliminado:", res.data)
                else:
                    print("Error:", res.error)
                get_res = hist.get_all()

            elif choice == '0':
                break
            else:
                print("Opción inválida.")