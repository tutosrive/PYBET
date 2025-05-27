from pybet.logic.WaitingQueue import WaitingQueue
from pybet.models.OperationResult import OperationResult

# Global instance of the queue
queue: WaitingQueue = WaitingQueue()

def manage_queue() -> None:
    """
    Manages the waiting queue: enqueue, dequeue and display contents.
    """
    while True:
        print("\n--- Waiting Queue ---")
        print("1. Enqueue Player")
        print("2. Dequeue Player")
        print("3. Show Queue")
        print("0. Back to main menu")
        option: str = input("Select an action: ").strip()

        if option == '1':
            player_id: str = input("Enter player ID to enqueue: ").strip()
            if player_id:
                queue.enqueue(player_id)
                print(f"Player {player_id} added to queue.")
            else:
                print("Player ID cannot be empty.")

        elif option == '2':
            result: OperationResult = queue.dequeue()
            if result.ok:
                print(f"Player {result.data} removed from the queue.")
            else:
                print("Queue is empty.")

        elif option == '3':
            current: list[str] = queue.get_all()
            if not current:
                print("Queue is empty.")
            else:
                print("Queue:")
                for i, name in enumerate(current, 1):
                    print(f"{i}. {name}")

        elif option == '0':
            break
        else:
            print("Invalid option.")
