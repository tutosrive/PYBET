from typing import Optional, List, Dict, Any
from pybet.models.Player import Player
from pybet.models.OperationResult import OperationResult
from pybet.models.DataPersistence import DataPersistence
from pybet.helpers.Helpers import Helpers


class PlayerManager:
    """
    Manages CRUD operations for Player entities, storing all players in a single
    JSON file (players.json) as a mapping from player_id → player data.

    Methods:
        - add_player: create and persist a new player with a readable unique ID.
        - get_all_players: return a list of all players.
        - get_player_by_name: find a player by name.
        - get_player_by_id: find a player by ID (binary search over loaded list).
        - update_player: change name and/or balance for an existing player.
        - delete_player: remove a player by ID.
    """

    def __init__(self) -> None:
        """
        Initializes the PlayerManager. No parameters required.
        """
        pass  # No state needed; each method loads/saves from DataPersistence.

    def add_player(self, name: str, balance: float) -> OperationResult:
        """
        Creates a new Player with a readable, non‐colliding ID and persists it.

        Args:
            name (str): Full name of the new player. Must be unique (case-insensitive).
            balance (float): Initial account balance (non-negative).

        Returns:
            OperationResult:
                ok (bool): True if creation succeeded.
                data (Player): The newly created Player object if ok.
                error (str): Error message otherwise.
        """
        # 1. Load existing mapping
        map_res = DataPersistence.load_players_map()
        if not map_res.ok:
            return map_res

        players_map: Dict[str, Any] = map_res.data

        # 2. Check duplicate name
        for p_dict in players_map.values():
            if p_dict.get("name", "").lower() == name.lower():
                return OperationResult(ok=False, error=f"Player '{name}' already exists.")

        # 3. Generate unique ID
        existing_ids = set(players_map.keys())
        new_id = Helpers.random_key(6)
        while new_id in existing_ids:
            new_id = Helpers.random_key(6)

        # 4. Instantiate Player object
        try:
            new_player = Player(
                player_id=new_id,
                name=name,
                account_balance=balance
            )
        except Exception as e:
            return OperationResult(ok=False, error=f"Error creating player: {e}")

        # 5. Insert into map and persist
        players_map[new_id] = new_player.to_dict()
        save_res = DataPersistence.save_players_map(players_map)
        if not save_res.ok:
            return save_res

        return OperationResult(ok=True, data=new_player)

    def get_all_players(self) -> OperationResult:
        """
        Retrieves a list of all Player objects from players.json.

        Returns:
            OperationResult:
                ok (bool): True if loaded successfully.
                data (List[Player]): List of all players if ok.
                error (str): Error message otherwise.
        """
        return DataPersistence.load_all_players()

    def get_player_by_name(self, name: str) -> OperationResult:
        """
        Finds a player by their full name (case-insensitive).

        Args:
            name (str): Full name to search for.

        Returns:
            OperationResult:
                ok (bool): True and data=Player if found.
                        False and error message otherwise.
        """
        all_res = self.get_all_players()
        if not all_res.ok:
            return all_res

        players: List[Player] = all_res.data
        for player in players:
            if player.name.lower() == name.lower():
                return OperationResult(ok=True, data=player)

        return OperationResult(ok=False, error=f"No player named '{name}' found.")

    def get_player_by_id(self, player_id: str) -> OperationResult:
        """
        Finds a player by their ID using binary search over the sorted list of IDs.

        Args:
            player_id (str): The unique ID to look up.

        Returns:
            OperationResult:
                ok (bool): True and data=Player if found.
                        False and error message otherwise.
        """
        all_res = self.get_all_players()
        if not all_res.ok:
            return all_res

        players: List[Player] = all_res.data
        # Sort players by ID for binary search
        players.sort(key=lambda p: p.id)
        low, high = 0, len(players) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_id = players[mid].id
            if mid_id == player_id:
                return OperationResult(ok=True, data=players[mid])
            elif mid_id < player_id:
                low = mid + 1
            else:
                high = mid - 1

        return OperationResult(ok=False, error=f"Player ID '{player_id}' not found.")

    def update_player(self, player_id: str, new_name: Optional[str] = None, new_balance: Optional[float] = None) -> OperationResult:
        """
        Updates an existing player's name and/or account balance.

        Args:
            player_id (str): The unique ID of the player to update.
            new_name (Optional[str]): New full name (if provided).
            new_balance (Optional[float]): New balance (≥ 0) if provided.

        Returns:
            OperationResult:
                ok (bool): True and data=updated Player on success.
                        False and error message otherwise.
        """
        # 1. Load mapping
        map_res = DataPersistence.load_players_map()
        if not map_res.ok:
            return map_res

        players_map: Dict[str, Any] = map_res.data
        if player_id not in players_map:
            return OperationResult(ok=False, error="Player not found.")

        # 2. Update fields
        record = players_map[player_id]
        if new_name:
            record["name"] = new_name
        if new_balance is not None:
            if new_balance < 0:
                return OperationResult(ok=False, error="Balance cannot be negative.")
            record["account_balance"] = new_balance

        # 3. Persist
        players_map[player_id] = record
        save_res = DataPersistence.save_players_map(players_map)
        if not save_res.ok:
            return save_res

        # 4. Return updated Player instance
        updated_player = Player.from_dict(record)
        return OperationResult(ok=True, data=updated_player)

    def delete_player(self, player_id: str) -> OperationResult:
        """
        Removes a player record from players.json by ID.

        Args:
            player_id (str): Unique ID of the player to delete.

        Returns:
            OperationResult:
                ok (bool): True and data=deleted Player on success.
                        False and error message otherwise.
        """
        # 1. Load mapping
        map_res = DataPersistence.load_players_map()
        if not map_res.ok:
            return map_res

        players_map: Dict[str, Any] = map_res.data
        if player_id not in players_map:
            return OperationResult(ok=False, error="Player not found.")

        # 2. Pop record
        record = players_map.pop(player_id)
        deleted_player = Player.from_dict(record)

        # 3. Persist
        save_res = DataPersistence.save_players_map(players_map)
        if not save_res.ok:
            return save_res

        return OperationResult(ok=True, data=deleted_player)
