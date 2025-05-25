import json
from pathlib import Path
from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult


class DataPersistence:
    """
    Provides methods to load and save Player data to JSON files.

    Attributes:
        file_path (Path): Path to the JSON file for persisting players.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes DataPersistence with the given file path.

        Args:
            file_path (str): Relative or absolute path to the JSON file.
        """
        self.file_path = Path(file_path)
        # Ensure the directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        # Create file if it does not exist
        if not self.file_path.exists():
            self.file_path.write_text('[]', encoding='utf-8')

    def load_players(self) -> OperationResult:
        """
        Loads all players from the JSON file.

        Returns:
            OperationResult: Success with list of Player instances, or failure with error.
        """
        try:
            with self.file_path.open('r', encoding='utf-8') as file:
                data = json.load(file)
            players: list[Player] = [Player.from_dict(item) for item in data]
            return OperationResult(success=True, data=players)
        except Exception as e:
            return OperationResult(success=False, error=e)

    def save_players(self, players: list[Player]) -> OperationResult:
        """
        Saves a list of Player instances to the JSON file.

        Args:
            players (list[Player]): List of players to persist.

        Returns:
            OperationResult: Success or failure with error.
        """
        try:
            serializable = [player.to_dict() for player in players]
            with self.file_path.open('w', encoding='utf-8') as file:
                json.dump(serializable, file, indent=4)
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=e)