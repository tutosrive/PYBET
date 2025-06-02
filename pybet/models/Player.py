from __future__ import annotations
from typing import Any, Dict, Optional, List
import datetime

class Player:
    """
    Represents a casino player with individual history.

    Attributes:
        id (str): Unique identifier.
        name (str): Full name.
        account_balance (float): Current balance.
        created_at (str): ISO timestamp of creation.
        history (List[str]): Last up to 10 actions.
    """

    def __init__(self,
                player_id: str,
                name: str,
                account_balance: float,
                created_at: Optional[str] = None,
                history: Optional[List[str]] = None) -> None:
        if account_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.id = player_id
        self.name = name
        self.account_balance = account_balance
        self.created_at = created_at or datetime.datetime.utcnow().isoformat()
        self.history: List[str] = history or []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Player:
        """
        Reconstructs a Player instance from a dictionary loaded from JSON.
        """
        return cls(
            player_id=data["id"],
            name=data["name"],
            account_balance=data["account_balance"],
            created_at=data.get("created_at"),
            history=data.get("history", [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Player instance to a dictionary for JSON serialization.

        Keeps only the last 10 history entries.
        """
        return {
            "id": self.id,
            "name": self.name,
            "account_balance": self.account_balance,
            "created_at": self.created_at,
            "history": self.history[-10:], # keep last 10
        }