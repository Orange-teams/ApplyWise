from pathlib import Path
from config.settings import DB_PATH


def reset_db():

    db_path = Path(DB_PATH)

    if db_path.exists():
        db_path.unlink()
        print("DB deleted")
    else:
        print("DB does not exist")


if __name__ == "__main__":
    reset_db()