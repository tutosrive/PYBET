from pathlib import Path
from pybet.main import main

# 1. Logs
Path("./pybet/logs").mkdir(parents=True, exist_ok=True)
Path("./pybet/logs/log.log").touch(exist_ok=True)

# 2. Data directory
Path("./pybet/data").mkdir(parents=True, exist_ok=True)

# 3. Initial data files
#    - players.json as JSON object null {}
#    - queue.json as null array []
for fname, initial_content in [("players.json", "{}"), ("queue.json", "[]")]:
    fpath = Path(f"./pybet/data/{fname}")
    if not fpath.exists():
        fpath.write_text(initial_content, encoding="utf-8")

if __name__ == "__main__":
    main()