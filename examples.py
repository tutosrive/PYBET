from pybet.models.PlayerManager import PlayerManager
from pybet.models.OperationResult import OperationResult
from pybet.logic.PlayerHistory import PlayerHistory
from pybet.helpers.FileManager import FileManager
import random
import os
import csv

DATA_DIR = './pybet/data/reports/'

def create_sample_players(manager: PlayerManager) -> list[str]:
    """
    Creates 3 example players with initial balances.
    
    Returns:
        list[str]: List of player IDs created.
    """
    print("📌 Creating example players...")
    ids = []
    for name, balance in [('Alice', 1000), ('Bob', 1500), ('Charlie', 1200)]:
        res = manager.add_player(name, balance)
        if res.ok:
            player = res.data
            ids.append(player.id)
            print(f'✅ Player created: {player.name} (ID: {player.id})')
        else:
            print(f'❌ Error creating player {name}: {res.error}')
    return ids

def simulate_slots(manager: PlayerManager, player_id: str) -> None:
    """
    Simulates a basic "slots" game.
    """
    bet = 200
    res = manager.get_player_by_id(player_id)
    if not res.ok:
        print(f'❌ Cannot find player {player_id}: {res.error}')
        return

    player = res.data
    if player.account_balance < bet:
        print(f'⚠️ Not enough balance for slots: {player.name}')
        return

    win = random.choice([True, False])
    reward = bet if win else -bet
    new_balance = player.account_balance + reward

    manager.update_player(player_id, new_balance=new_balance)
    msg = (f'Tragamonedas (Slots): Apostó {bet}, {"ganó" if win else "perdió"} {abs(reward)}, saldo {new_balance}')
    
    PlayerHistory(player_id).push(msg)
    print(f'🎰 {player.name}: {msg}')

def simulate_guessing(manager: PlayerManager, player_id: str) -> None:
    """
    Simulates a basic "guessing" game.
    """
    bet = 150
    res = manager.get_player_by_id(player_id)
    if not res.ok:
        print(f'❌ Cannot find player {player_id}: {res.error}')
        return

    player = res.data
    if player.account_balance < bet:
        print(f'⚠️ Not enough balance for guessing: {player.name}')
        return

    secret = random.randint(1, 5)
    guess = random.randint(1, 5)

    if guess == secret:
        reward = bet * 4
        new_balance = player.account_balance + reward
        outcome = f'ganó {reward}'
    else:
        reward = -bet
        new_balance = player.account_balance + reward
        outcome = f'perdió {bet} (salió {secret})'

    manager.update_player(player_id, new_balance=new_balance)
    msg = (f'Adivinanzas: Apostó {bet}, eligió {guess}, {outcome}, saldo {new_balance}')

    PlayerHistory(player_id).push(msg)
    print(f'🧠 {player.name}: {msg}')


def export_player_history(player_id: str) -> None:
    """
    Exports a player's history to CSV and JSON in /reports.
    """
    hist = PlayerHistory(player_id)
    data_res = hist.get_all()
    if not data_res.ok:
        print(f'❌ Error loading history: {data_res.error}')
        return

    history = data_res.data
    if not history:
        print(f'⚠️ No history to export for player {player_id}')
        return

    # Export JSON
    json_path = os.path.join(DATA_DIR, f'history_{player_id}.json')
    FileManager.write_file(json_path, history)

    # Export CSV
    csv_path = os.path.join(DATA_DIR, f'history_{player_id}.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Action'])
        for entry in history:
            writer.writerow([entry])

    print(f'📤 History exported for {player_id} → JSON/CSV')


if __name__ == '__main__':
    print("🔍 Starting example script for ROL B...")
    manager = PlayerManager()

    ids = create_sample_players(manager)

    for pid in ids:
        simulate_slots(manager, pid)
        simulate_guessing(manager, pid)
        export_player_history(pid)

    print("\n✅ Example simulation completed.")