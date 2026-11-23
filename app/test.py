from pathlib import Path
import init_database as init_db
import sqlite3
current_dir = Path(__file__).resolve().parent
UD = current_dir  / "UD.json"
his= current_dir / "history"
data_base=his/"history.db"

x=init_db.file_path(data_base)
print(x)