from typing import List
from pybet.helpers.FileManager import FileManager
from pybet.models.OperationResult import OperationResult
from pybet.models.DataPersistence import DataPersistence

class PlayerHistory:
    """
    Manages a single player's action history within players.json.
    """

    def __init__(self, player_id: str, max_size: int = 10) -> None:
        self.player_id = player_id
        self.max_size = max_size

    def _load_map(self) -> OperationResult:
        return DataPersistence.load_players_map()

    def push(self, action: str) -> OperationResult:
        """
        Appends an action to that player's history (capping at max_size).
        """
        map_res = self._load_map()
        if not map_res.ok:
            return map_res

        players_map = map_res.data
        if self.player_id not in players_map:
            return OperationResult(ok=False, error="Player not found.")

        # Update history
        hist = players_map[self.player_id].get("history", [])
        hist.append(action)
        hist = hist[-self.max_size:]
        players_map[self.player_id]["history"] = hist

        return DataPersistence.save_players_map(players_map)

    def pop(self) -> OperationResult:
        """
        Removes and returns the last action.
        """
        map_res = self._load_map()
        if not map_res.ok:
            return map_res

        pm = map_res.data
        if self.player_id not in pm:
            return OperationResult(ok=False, error="Player not found.")

        hist = pm[self.player_id].get("history", [])
        if not hist:
            return OperationResult(ok=False, error="No history.")
        action = hist.pop()
        pm[self.player_id]["history"] = hist
        save_res = DataPersistence.save_players_map(pm)
        return OperationResult(ok=save_res.ok, data=action, error=save_res.error)

    def get_all(self) -> OperationResult:
        """
        Retrieves the full history list for the player.
        """
        map_res = self._load_map()
        if not map_res.ok:
            return map_res
        pm = map_res.data
        if self.player_id not in pm:
            return OperationResult(ok=False, error="Player not found.")
        return OperationResult(ok=True, data=pm[self.player_id].get("history", []))