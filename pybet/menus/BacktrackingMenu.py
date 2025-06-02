from typing import List
from pybet.logic.Backtracking import Backtracking
from pybet.models.OperationResult import OperationResult

def optimal_betting_path() -> None:
    """
    Menu to compute the optimal betting path (subset-sum) for a given balance
    and list of bet options.
    """
    while True:
        print("\n--- Camino Óptimo de Apuestas ---")
        print("1. Calcular apuestas óptimas")
        print("0. Volver al menú principal")
        choice: str = input("Seleccione una opción: ").strip()

        if choice == '1':
            bal_str: str = input("Ingrese saldo inicial (entero): ").strip()
            try:
                initial_balance: int = int(bal_str)
            except ValueError:
                print("Saldo inválido. Debe ser un número entero.")
                continue

            opts_str: str = input(
                "Ingrese opciones de apuesta separadas por coma (ej. 5,10,20): "
            ).strip()
            try:
                bet_options: List[int] = [
                    int(x.strip()) for x in opts_str.split(',') if x.strip()
                ]
            except ValueError:
                print("Opciones inválidas. Asegúrese de ingresar números enteros separados por coma.")
                continue

            solver = Backtracking(initial_balance, bet_options)
            best_seq, best_total = solver.findOptimalPath()
            print(f"\nSaldo inicial: {initial_balance}")
            print(f"Opciones de apuesta: {bet_options}")
            print(f"Secuencia óptima de apuestas: {best_seq}")
            print(f"Monto total apostado: {best_total}")

        elif choice == '0':
            break
        else:
            print("Opción inválida, intente de nuevo.")