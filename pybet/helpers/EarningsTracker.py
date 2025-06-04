"""
EarningsTracker module for tracking and updating player earnings.

This module provides the EarningsTracker class, which offers static methods to update and retrieve player earnings stored in a JSON file. It ensures the earnings file is created if it does not exist and handles invalid or missing data gracefully.
"""

import json
import os

EARNINGS_FILE = './pybet/data/reports/earnings_totals.json'

class EarningsTracker:
    @staticmethod
    def update_earnings(player_id: str, amount: float) -> None:
        """
        Update the earnings for a given player by adding the specified amount.

        Args:
            player_id (str): The unique identifier for the player.
            amount (float): The amount to add to the player's earnings.
        """
        earnings = {}
        if os.path.exists(EARNINGS_FILE):
            with open(EARNINGS_FILE, 'r', encoding='utf-8') as f:
                try:
                    earnings = json.load(f)
                except json.JSONDecodeError:
                    earnings = {}

        earnings[player_id] = earnings.get(player_id, 0.0) + amount

        with open(EARNINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(earnings, f, indent=4)

    @staticmethod
    def get_all_earnings() -> dict:
        """
        Retrieve all player earnings as a dictionary.

        Returns:
            dict: A dictionary mapping player IDs to their total earnings. Returns an empty dictionary if the file does not exist or is invalid.
        """
        if not os.path.exists(EARNINGS_FILE):
            return {}
        with open(EARNINGS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}