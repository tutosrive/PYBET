from pybet.logic.WaitingQueue import WaitingQueue
from pybet.models.OperationResult import OperationResult

# Global instance of the queue
queue: WaitingQueue = WaitingQueue()

def manage_queue() -> None:
    """
    Manages the waiting queue: enqueue, dequeue, and display contents.
    """
    while True:
        print("\n--- Manejar Cola de Espera ---")
        print("1. Encolar jugador")
        print("2. Desencolar jugador")
        print("3. Mostrar cola")
        print("0. Volver al menú principal")
        option: str = input("Seleccione una opción: ").strip()

        if option == '1':
            player_id: str = input("Ingrese ID de jugador para encolar: ").strip()
            if player_id:
                queue.enqueue(player_id)
                print(f"Jugador {player_id} agregado a la cola.")
            else:
                print("El ID de jugador no puede estar vacío.")

        elif option == '2':
            result: OperationResult = queue.dequeue()
            if result.ok:
                print(f"Jugador {result.data} removido de la cola.")
            else:
                print("La cola está vacía.")

        elif option == '3':
            current: list[str] = queue.get_all()
            if not current:
                print("La cola está vacía.")
            else:
                print("Cola:")
                for i, pid in enumerate(current, 1):
                    print(f"{i}. {pid}")

        elif option == '0':
            break
        else:
            print("Opción inválida.")