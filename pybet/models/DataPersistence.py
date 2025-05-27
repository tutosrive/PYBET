from pathlib import Path
from typing import List, Optional
from pybet.helpers.FileManager import FileManager
from pybet.models.OperationResult import OperationResult
from pybet.models.Player import Player

class DataPersistence:
    """
    Manages loading and saving of Player data via JSON files.

    Attributes:
        DATA_FILE (str): Default path to the players JSON file.
    """

    DATA_FILE: str = './pybet/data/players.json'

    @staticmethod
    def load_players(data_file: Optional[str] = None) -> OperationResult:
        """
        Reads the JSON file at DATA_FILE (or at data_file if provided),
        parses it into Player objects.

        If the file does not exist, creates it as an empty JSON list.

        Args:
            data_file (Optional[str]): Override path to JSON file.

        Returns:
            OperationResult:
                ok (bool): True if read+parsed successfully.
                data (List[Player]): On success, list of Player instances.
                error (str): Error message on failure.
        """
        path_str = data_file if data_file else DataPersistence.DATA_FILE
        path = Path(path_str)
        if not path.exists():
            # inicializar como lista vacía
            FileManager.write_file(path_str, [], mode='w')

        raw = FileManager.read_file_json(path_str)
        if not raw.ok:
            return OperationResult(ok=False, error=raw.error)

        try:
            players = [Player.from_dict(d) for d in raw.data]
            return OperationResult(ok=True, data=players)
        except Exception as e:
            return OperationResult(ok=False, error=f'Error parsing player data: {e}')

    @staticmethod
    def save_players(players: List[Player], data_file: Optional[str] = None) -> OperationResult:
        """
        Serializes a list of Player instances to JSON and writes it to DATA_FILE
        (or to data_file if provided).

        Args:
            players (List[Player]): The list of players to save.
            data_file (Optional[str]): Override path to JSON file.

        Returns:
            OperationResult:
                ok (bool): True if written successfully.
                error (str): Error message on failure.
        """
        path_str = data_file if data_file else DataPersistence.DATA_FILE
        try:
            payload = [p.to_dict() for p in players]
            write_res = FileManager.write_file(path_str, payload, mode='w')
            if write_res.ok:
                return OperationResult(ok=True)
            else:
                return OperationResult(ok=False, error=write_res.error)
        except Exception as e:
            return OperationResult(ok=False, error=f'Error saving player data: {e}')
