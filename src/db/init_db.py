from src.db.base import Base
from src.db.session import engine
from src.db import models  # IMPORTANT: ensures models are registered
from config.settings import DB_URL, DB_PATH


def init_db():

    # Ensure DB folder exists
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)