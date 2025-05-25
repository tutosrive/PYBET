class HistoryStack:
    """
    Implements a simple stack to track the last N actions for a player.

    Attributes:
        max_size (int): Maximum number of actions to retain.
        stack (list[str]): Internal list storing action descriptions.
    """

    def __init__(self, max_size: int = 10) -> None:
        """
        Initializes the HistoryStack with a given maximum size.

        Args:
            max_size (int): The maximum number of actions the stack holds.
                            Defaults to 10.
        """
        self.max_size: int = max_size
        self.stack: list[str] = []

    def push(self, action: str) -> None:
        """
        Pushes a new action onto the stack. If the stack exceeds max_size,
        removes the oldest action.

        Args:
            action (str): A description of the action (e.g., "Bet $50 on slots").
        """
        self.stack.append(action)
        if len(self.stack) > self.max_size:
            # Discard the oldest action
            self.stack.pop(0)

    def pop(self) -> str:
        """
        Pops the most recent action from the stack.

        Returns:
            str: The last action description.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.stack:
            raise IndexError("No actions in history.")
        return self.stack.pop()

    def peek(self) -> str:
        """
        Returns the most recent action without removing it.

        Returns:
            str: The last action description.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.stack:
            raise IndexError("No actions in history.")
        return self.stack[-1]

    def is_empty(self) -> bool:
        """
        Checks if the history stack is empty.

        Returns:
            bool: True if empty, False otherwise.
        """
        return not self.stack

    def clear(self) -> None:
        """
        Clears all actions from the history.
        """
        self.stack.clear()
