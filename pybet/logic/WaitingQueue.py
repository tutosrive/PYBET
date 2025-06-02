from typing import List
from pybet.helpers.FileManager import FileManager
from pybet.models.OperationResult import OperationResult

QUEUE_FILE = './pybet/data/queue.json'

class WaitingQueue:
    """
    Implements a basic FIFO queue to manage player IDs,
    persisted to queue.json.
    """

    def __init__(self) -> None:
        read_res = FileManager.read_file_json(QUEUE_FILE)
        if read_res.ok and isinstance(read_res.data, list):
            self.queue: List[str] = read_res.data
        else:
            self.queue = []

    def _persist(self) -> None:
        FileManager.write_file(QUEUE_FILE, self.queue, mode='w')

    def enqueue(self, player_id: str) -> OperationResult:
        """
        Adds a player ID to the end of the queue.
        """
        self.queue.append(player_id)
        self._persist()
        return OperationResult(ok=True)

    def dequeue(self) -> OperationResult:
        """
        Removes and returns the player ID at the front of the queue.
        """
        if not self.queue:
            return OperationResult(ok=False, error="Queue is empty.")
        pid = self.queue.pop(0)
        self._persist()
        return OperationResult(ok=True, data=pid)

    def peek(self) -> OperationResult:
        """
        Returns the player ID at the front without removing it.
        """
        if not self.queue:
            return OperationResult(ok=False, error="Queue is empty.")
        return OperationResult(ok=True, data=self.queue[0])

    def get_all(self) -> List[str]:
        """
        Returns a copy of the entire queue.
        """
        return self.queue.copy()

    def clear(self) -> OperationResult:
        """
        Empties the queue.
        """
        self.queue.clear()
        self._persist()
        return OperationResult(ok=True)