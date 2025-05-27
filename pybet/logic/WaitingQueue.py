from typing import List
from pybet.helpers.FileManager import FileManager
from pybet.models.OperationResult import OperationResult

QUEUE_FILE = './pybet/data/queue.json'

class WaitingQueue:
    def __init__(self) -> None:
        # run.py ya creó queue.json con "[]"
        res = FileManager.read_file_json(QUEUE_FILE)
        if res.ok and isinstance(res.data, list):
            self.queue: List[str] = res.data
        else:
            self.queue = []

    def _persist(self) -> None:
        FileManager.write_file(QUEUE_FILE, self.queue, mode='w')

    def enqueue(self, player_id: str) -> OperationResult:
        self.queue.append(player_id)
        self._persist()
        return OperationResult(ok=True)

    def dequeue(self) -> OperationResult:
        if not self.queue:
            return OperationResult(ok=False, error="Queue is empty.")
        pid = self.queue.pop(0)
        self._persist()
        return OperationResult(ok=True, data=pid)

    def peek(self) -> OperationResult:
        if not self.queue:
            return OperationResult(ok=False, error="Queue is empty.")
        return OperationResult(ok=True, data=self.queue[0])

    def get_all(self) -> List[str]:
        return self.queue.copy()

    def clear(self) -> OperationResult:
        self.queue.clear()
        self._persist()
        return OperationResult(ok=True)