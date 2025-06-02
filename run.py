from pathlib import Path
from pybet.main import main

# 1. Create logs directory and log file
Path("./pybet/logs").mkdir(parents=True, exist_ok=True)
Path("./pybet/logs/log.log").touch(exist_ok=True)

# 2. Create data directory
Path("./pybet/data").mkdir(parents=True, exist_ok=True)

# 3. Initial data files:
#    - players.json: empty JSON object {}
#    - queue.json:   empty JSON array []
for fname, initial_content in [("players.json", "{}"), ("queue.json", "[]")]:
    fpath = Path(f"./pybet/data/{fname}")
    if not fpath.exists():
        fpath.write_text(initial_content, encoding="utf-8")

if __name__ == "__main__":
    main()