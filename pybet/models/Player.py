from pybet.helpers.FileManager import FileManager
import uuid

class Player:
    """
    Represents a casino player with a unique identifier, name, and account balance.

    Attributes:
        id (str): Unique identifier for the player.
        name (str): Full name of the player.
        account_balance (float): Current balance of the player's account (must be non-negative).
    """

    def __init__(self, name: str, account_balance: float) -> None:
        if account_balance < 0:
            raise ValueError("Account balance cannot be negative.")
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.account_balance: float = account_balance

    def to_dict(self) -> dict:
        """
        Converts the Player instance to a dictionary for JSON serialization.

        Returns:
            dict: A dictionary representation of the player.
        """
        return {
            "id": self.id,
            "name": self.name,
            "account_balance": self.account_balance
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """
        Creates a Player instance from a dictionary.

        Args:
            data (dict): Dictionary with keys 'id', 'name', and 'account_balance'.

        Returns:
            Player: A new Player instance.
        """
        player = cls(name=data["name"], account_balance=data["account_balance"])
        player.id = data["id"]  # preserve original ID
        return player