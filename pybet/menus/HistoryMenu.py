from typing import Optional, List
from pybet.logic.HistoryStack import HistoryStack
from pybet.models.OperationResult import OperationResult

def view_history() -> None:
    """
    Menu to interact with the global history stack.
    """
    history: HistoryStack = HistoryStack()

    while True:
        print("\n--- Player History Stack ---")
        print("1. Push action")
        print("2. Pop last action")
        print("3. Peek last action")
        print("4. Show entire stack")
        print("0. Back to main menu")
        choice: str = input("Choose an action: ").strip()

        if choice == '1':
            action: str = input("Enter action description: ").strip()
            if action:
                history.push(action)
                print(f"Action pushed: {action}")
            else:
                print("Action cannot be empty.")

        elif choice == '2':
            try:
                last_action: str = history.pop()
                print(f"Popped action: {last_action}")
            except IndexError as e:
                print("Error:", e)

        elif choice == '3':
            try:
                last_action: str = history.peek()
                print(f"Last action: {last_action}")
            except IndexError as e:
                print("Error:", e)

        elif choice == '4':
            stack: List[str] = history.stack
            if not stack:
                print("History is empty.")
            else:
                print("History stack (oldest→newest):")
                for idx, act in enumerate(stack, 1):
                    print(f"{idx}. {act}")

        elif choice == '0':
            break

        else:
            print("Invalid option, try again.")