from typing import List
from pybet.helpers.FileManager import FileManager

HISTORY_FILE = './pybet/data/history.json'

class HistoryStack:
    """
    A stack of recent actions, persisted to history.json.
    """

    def __init__(self, max_size: int = 10) -> None:
        self.max_size = max_size
        # Dado que run.py ya inicializó history.json como "[]",
        # podemos leerlo sin error.
        res = FileManager.read_file_json(HISTORY_FILE)
        if res.ok and isinstance(res.data, list):
            self.stack: List[str] = res.data[-self.max_size:]
        else:
            # Si por algún motivo falla, arrancamos vacío
            self.stack = []

    def _persist(self) -> None:
        FileManager.write_file(HISTORY_FILE, self.stack, mode='w')

    def push(self, action: str) -> None:
        self.stack.append(action)
        if len(self.stack) > self.max_size:
            self.stack.pop(0)
        self._persist()

    def pop(self) -> str:
        if not self.stack:
            raise IndexError("No actions in history.")
        val = self.stack.pop()
        self._persist()
        return val

    def peek(self) -> str:
        if not self.stack:
            raise IndexError("No actions in history.")
        return self.stack[-1]

    def clear(self) -> None:
        self.stack.clear()
        self._persist()