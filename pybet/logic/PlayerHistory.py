from typing import List
from pybet.helpers.FileManager import FileManager
from pybet.models.OperationResult import OperationResult
from pybet.models.DataPersistence import DataPersistence

class PlayerHistory:
    """
    Manages a single player's action history embedded in players.json.
    """

    def __init__(self, player_id: str, max_size: int = 10) -> None:
        self.player_id = player_id
        self.max_size = max_size

    def _load_map(self) -> OperationResult:
        return DataPersistence.load_players_map()

    def push(self, action: str) -> OperationResult:
        """
        Appends an action to the player's history (keeping only last max_size entries).

        Returns:
            OperationResult: ok=True if saved; data=None; error otherwise.
        """
        map_res = self._load_map()
        if not map_res.ok:
            return map_res

        players_map = map_res.data
        if self.player_id not in players_map:
            return OperationResult(ok=False, error="Player not found.")

        history_list: List[str] = players_map[self.player_id].get("history", [])
        history_list.append(action)
        # Keep only last `max_size`
        history_list = history_list[-self.max_size:]
        players_map[self.player_id]["history"] = history_list

        return DataPersistence.save_players_map(players_map)

    def pop(self) -> OperationResult:
        """
        Removes and returns the last action from the player's history.

        Returns:
            OperationResult: ok=True and data=string of popped action; error otherwise.
        """
        map_res = self._load_map()
        if not map_res.ok:
            return map_res

        players_map = map_res.data
        if self.player_id not in players_map:
            return OperationResult(ok=False, error="Player not found.")

        history_list: List[str] = players_map[self.player_id].get("history", [])
        if not history_list:
            return OperationResult(ok=False, error="No history.")
        action = history_list.pop()
        players_map[self.player_id]["history"] = history_list

        save_res = DataPersistence.save_players_map(players_map)
        return OperationResult(ok=save_res.ok, data=action, error=save_res.error)

    def get_all(self) -> OperationResult:
        """
        Retrieves the full history list for the player.

        Returns:
            OperationResult: ok=True and data=List[str] if exists; error otherwise.
        """
        map_res = self._load_map()
        if not map_res.ok:
            return map_res
        players_map = map_res.data
        if self.player_id not in players_map:
            return OperationResult(ok=False, error="Player not found.")
        return OperationResult(ok=True, data=players_map[self.player_id].get("history", []))