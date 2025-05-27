from typing import Optional, List

from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult
from pybet.models.DataPersistence import DataPersistence

class PlayerManager:
    """
    Provides CRUD operations for Player entities.

    You can override the JSON file path by passing a custom data_file
    when constructing this manager.
    """

    def __init__(self, data_file: Optional[str] = None) -> None:
        """
        Initializes the PlayerManager.

        Args:
            data_file (Optional[str]): Path to the JSON file storing players. If omitted, uses DataPersistence.DATA_FILE.
        """
        self.data_file = data_file

    def add_player(self, name: str, balance: float) -> OperationResult:
        """
        Creates a new Player and persists it.

        Args:
            name (str): Full name of the player.
            balance (float): Initial account balance (must be >= 0).

        Returns:
            OperationResult:
                ok (bool): True and data=Player on success.
                        False and error message on failure.
        """
        load_res = DataPersistence.load_players(self.data_file)
        if not load_res.ok:
            return load_res

        try:
            existing: List[Player] = load_res.data
            new_player = Player(name=name, account_balance=balance)
            existing.append(new_player)
            save_res = DataPersistence.save_players(existing, self.data_file)
            if not save_res.ok:
                return save_res
            return OperationResult(ok=True, data=new_player)
        except Exception as e:
            return OperationResult(ok=False, error=f'Error adding player: {e}')

    def get_all_players(self) -> OperationResult:
        """
        Retrieves all Player records.

        Returns:
            OperationResult:
                ok (bool): True and data=List[Player] on success.
                        False and error message on failure.
        """
        return DataPersistence.load_players(self.data_file)
    
    def get_player_by_name(self, name: str) -> OperationResult:
        """
        Finds a player by full name using linear search.

        Args:
            name (str): Name to search (case-insensitive).

        Returns:
            OperationResult:
                ok (bool): True and data=Player if found.
                        False and error message if not found.
        """
        load_res = DataPersistence.load_players(self.data_file)
        if not load_res.ok:
            return load_res

        for p in load_res.data:
            if p.name.lower() == name.lower():
                return OperationResult(ok=True, data=p)

        return OperationResult(ok=False, error=f"Player with name '{name}' not found")

    def get_player_by_id(self, player_id: str) -> OperationResult:
        """
        Finds a player by UUID using binary search over sorted IDs.

        Args:
            player_id (str): The UUID string of the player.

        Returns:
            OperationResult:
                ok (bool): True and data=Player if found.
                        False and error message otherwise.
        """
        load_res = DataPersistence.load_players(self.data_file)
        if not load_res.ok:
            return load_res

        players: List[Player] = sorted(load_res.data, key=lambda p: p.id)
        low, high = 0, len(players) - 1
        while low <= high:
            mid = (low + high) // 2
            if players[mid].id == player_id:
                return OperationResult(ok=True, data=players[mid])
            if players[mid].id < player_id:
                low = mid + 1
            else:
                high = mid - 1

        return OperationResult(ok=False, error=f"Player with ID '{player_id}' not found")

    def update_player(self, player_id: str, new_name: Optional[str] = None, new_balance: Optional[float] = None) -> OperationResult:
        """
        Updates an existing player's name and/or balance.

        Args:
            player_id (str): UUID of the player to update.
            new_name (Optional[str]): New full name.
            new_balance (Optional[float]): New balance (>= 0).

        Returns:
            OperationResult:
                ok (bool): True and data=updated Player on success.
                        False and error message on failure.
        """
        load_res = DataPersistence.load_players(self.data_file)
        if not load_res.ok:
            return load_res

        players: List[Player] = load_res.data
        for p in players:
            if p.id == player_id:
                if new_name:
                    p.name = new_name
                if new_balance is not None:
                    if new_balance < 0:
                        return OperationResult(ok=False, error="Balance cannot be negative")
                    p.account_balance = new_balance

                save_res = DataPersistence.save_players(players, self.data_file)
                return save_res.ok and OperationResult(ok=True, data=p) or save_res

        return OperationResult(ok=False, error=f"Player with ID '{player_id}' not found")

    def delete_player(self, player_id: str) -> OperationResult:
        """
        Deletes a player by UUID.

        Args:
            player_id (str): UUID of the player to delete.

        Returns:
            OperationResult:
                ok (bool): True and data=deleted Player on success.
                        False and error message on failure.
        """
        load_res = DataPersistence.load_players(self.data_file)
        if not load_res.ok:
            return load_res

        players: List[Player] = load_res.data
        for idx, p in enumerate(players):
            if p.id == player_id:
                removed = players.pop(idx)
                save_res = DataPersistence.save_players(players, self.data_file)
                return save_res.ok and OperationResult(ok=True, data=removed) or save_res

        return OperationResult(ok=False, error=f"Player with ID '{player_id}' not found")