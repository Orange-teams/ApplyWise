from pathlib import Path
import random

from src.db.init_db import init_db
from src.db.session import SessionLocal
from src.db.models import User, Keyword
from config.settings import settings, DB_PATH
from config.settings import DB_PATH

def db_exists() -> bool:
    return Path(DB_PATH).exists()


def seed_db():
    session = SessionLocal()

    try:
        # create a fake user
        user = User(name=f"user_1")
        session.add(user)
        session.flush()

        # random keywords
        all_keywords = [
            "Python"
        ]

        for kw in all_keywords:
            session.add(Keyword(
                user_id=user.id,
                value=kw
            ))

        session.commit()

    finally:
        session.close()


def bootstrap_db():

    init_db()

    # check if database already has data
    session = SessionLocal()

    try:
        existing_user = session.query(User).first()

        if existing_user:
            return

    finally:
        session.close()

    seed_db()