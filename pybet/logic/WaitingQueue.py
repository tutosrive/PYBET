class WaitingQueue:
    """
    Implements a basic FIFO queue to manage players waiting for a game.

    Attributes:
        queue (list[str]): Internal list storing player IDs in arrival order.
    """

    def __init__(self) -> None:
        """
        Initializes an empty waiting queue.
        """
        self.queue: list[str] = []

    def enqueue(self, player_id: str) -> None:
        """
        Adds a player ID to the end of the queue.

        Args:
            player_id (str): The unique identifier of the player.
        """
        self.queue.append(player_id)

    def dequeue(self) -> str:
        """
        Removes and returns the player ID at the front of the queue.

        Returns:
            str: The player ID that was waiting the longest.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty waiting queue.")
        return self.queue.pop(0)

    def peek(self) -> str:
        """
        Returns the player ID at the front without removing it.

        Returns:
            str: The next player ID to be served.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty waiting queue.")
        return self.queue[0]

    def is_empty(self) -> bool:
        """
        Checks if the queue has no players.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.queue) == 0

    def clear(self) -> None:
        """
        Empties the queue.
        """
        self.queue.clear()
