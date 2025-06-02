from pathlib import Path
from typing import Dict, Any, List

from pybet.helpers.FileManager import FileManager
from pybet.models.OperationResult import OperationResult
from pybet.models.Player import Player

PLAYERS_FILE = './pybet/data/players.json'

class DataPersistence:
    """
    Manages loading and saving of all player data in one JSON mapping.
    Each player is stored under their unique ID as key.
    """

    @staticmethod
    def load_players_map() -> OperationResult:
        """
        Loads the full players.json as a mapping id → player-dict.

        Returns:
            OperationResult:
                ok (bool): True if load succeeded.
                data (Dict[str, Any]): Mapping of all players if ok.
                error (str): Error message otherwise.
        """
        # Ensure directory exists
        Path(PLAYERS_FILE).parent.mkdir(parents=True, exist_ok=True)
        # If file does not exist, initialize as empty dict
        if not Path(PLAYERS_FILE).exists():
            FileManager.write_file(PLAYERS_FILE, {}, mode='w')

        raw = FileManager.read_file_json(PLAYERS_FILE)
        if not raw.ok:
            return raw

        data = raw.data
        if not isinstance(data, dict):
            return OperationResult(ok=False, error="players.json corrupted (expected a JSON object).")
        return OperationResult(ok=True, data=data)

    @staticmethod
    def save_players_map(players_map: Dict[str, Any]) -> OperationResult:
        """
        Persists the entire mapping to players.json.

        Args:
            players_map (Dict[str, Any]): The full mapping of players.

        Returns:
            OperationResult: ok=True if save succeeded; error otherwise.
        """
        return FileManager.write_file(PLAYERS_FILE, players_map, mode='w')

    @staticmethod
    def load_all_players() -> OperationResult:
        """
        Returns a list of Player instances built from the mapping.

        Returns:
            OperationResult:
                ok (bool): True if load+parse succeeded.
                data (List[Player]): List of all Player objects if ok.
                error (str): Error message otherwise.
        """
        map_res = DataPersistence.load_players_map()
        if not map_res.ok:
            return map_res

        try:
            players = [Player.from_dict(v) for v in map_res.data.values()]
            return OperationResult(ok=True, data=players)
        except Exception as e:
            return OperationResult(ok=False, error=f"Error parsing players: {e}")