from typing import Optional

from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult
from pybet.models.DataPersistence import DataPersistence

class PlayerManager:
    """
    Manages CRUD operations for Player instances using JSON persistence.

    Attributes:
        persistence (DataPersistence): Instance for loading and saving players.
    """

    def __init__(self, data_file: str) -> None:
        """
        Initializes PlayerManager with the given data file path.

        Args:
            data_file (str): Path to the JSON file storing player data.
        """
        self.persistence = DataPersistence(data_file)

    def add_player(self, name: str, balance: float) -> OperationResult:
        """
        Creates and persists a new player.

        Args:
            name (str): Full name of the new player.
            balance (float): Initial account balance (must be non-negative).

        Returns:
            OperationResult: success with Player on success; error otherwise.
        """
        try:
            # Load existing players
            result = self.persistence.load_players()
            if not result.success:
                return result
            players: list[Player] = result.data

            # Create new player and append
            new_player = Player(name=name, account_balance=balance)
            players.append(new_player)

            # Save updated list
            save_result = self.persistence.save_players(players)
            if not save_result.success:
                return save_result

            return OperationResult(success=True, data=new_player)
        except Exception as e:
            return OperationResult(success=False, error=e)

    def get_all_players(self) -> OperationResult:
        """
        Retrieves all persisted players.

        Returns:
            OperationResult: success with list[Player] on success; error otherwise.
        """
        return self.persistence.load_players()

    def get_player_by_name(self, name: str) -> OperationResult:
        """
        Finds a player by full name using linear search.

        Args:
            name (str): Full name to search for.

        Returns:
            OperationResult: success with Player if found; error if not or on failure.
        """
        result = self.persistence.load_players()
        if not result.success:
            return result
        players: list[Player] = result.data

        # Linear search
        for player in players:
            if player.name.lower() == name.lower():
                return OperationResult(success=True, data=player)

        return OperationResult(success=False, error=ValueError(f"Player with name '{name}' not found."))

    def get_player_by_id(self, player_id: str) -> OperationResult:
        """
        Finds a player by ID using binary search over a sorted list.

        Args:
            player_id (str): UUID string of the player.

        Returns:
            OperationResult: success with Player if found; error if not or on failure.
        """
        result = self.persistence.load_players()
        if not result.success:
            return result
        players: list[Player] = result.data

        # Sort players by ID for binary search
        players.sort(key=lambda p: p.id)

        low, high = 0, len(players) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_id = players[mid].id
            if mid_id == player_id:
                return OperationResult(success=True, data=players[mid])
            elif mid_id < player_id:
                low = mid + 1
            else:
                high = mid - 1

        return OperationResult(success=False, error=ValueError(f"Player with ID '{player_id}' not found."))

    def update_player(self, player_id: str, new_name: Optional[str] = None, new_balance: Optional[float] = None) -> OperationResult:
        """
        Updates name and/or account balance of an existing player.

        Args:
            player_id (str): UUID of the player to update.
            new_name (Optional[str]): New full name (if provided).
            new_balance (Optional[float]): New balance (if provided, must be non-negative).

        Returns:
            OperationResult: success with updated Player; error otherwise.
        """
        load_result = self.persistence.load_players()
        if not load_result.success:
            return load_result
        players: list[Player] = load_result.data

        for idx, player in enumerate(players):
            if player.id == player_id:
                if new_name:
                    player.name = new_name
                if new_balance is not None:
                    if new_balance < 0:
                        return OperationResult(success=False, error=ValueError("Balance cannot be negative."))
                    player.account_balance = new_balance

                save_result = self.persistence.save_players(players)
                if not save_result.success:
                    return save_result

                return OperationResult(success=True, data=player)

        return OperationResult(success=False, error=ValueError(f"Player with ID '{player_id}' not found."))

    def delete_player(self, player_id: str) -> OperationResult:
        """
        Removes a player from persistence by ID.

        Args:
            player_id (str): UUID of the player to delete.

        Returns:
            OperationResult: success with deleted Player; error otherwise.
        """
        load_result = self.persistence.load_players()
        if not load_result.success:
            return load_result
        players: list[Player] = load_result.data

        for idx, player in enumerate(players):
            if player.id == player_id:
                deleted = players.pop(idx)
                save_result = self.persistence.save_players(players)
                if not save_result.success:
                    return save_result
                return OperationResult(success=True, data=deleted)

        return OperationResult(success=False, error=ValueError(f"Player with ID '{player_id}' not found."))
