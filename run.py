from pathlib import Path
from pybet.main import main

# Create necessary directories and files for the application
# Logs
Path("./pybet/logs").mkdir(parents=True, exist_ok=True)
Path("./pybet/logs/log.log").touch(exist_ok=True)

# Data
Path("./pybet/data").mkdir(parents=True, exist_ok=True)
for fname in ("players.json", "history.json", "queue.json"):
    fpath = Path(f"./pybet/data/{fname}")
    if not fpath.exists():
        fpath.write_text("[]", encoding="utf-8")

if __name__ == "__main__":
    main()