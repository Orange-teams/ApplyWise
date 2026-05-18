from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import DB_URL

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)