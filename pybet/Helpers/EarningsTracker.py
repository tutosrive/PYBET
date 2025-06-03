import json
import os

EARNINGS_FILE = './pybet/data/reports/earnings_totals.json'

class EarningsTracker:
    @staticmethod
    def update_earnings(player_id: str, amount: float) -> None:
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
        if not os.path.exists(EARNINGS_FILE):
            return {}
        with open(EARNINGS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}