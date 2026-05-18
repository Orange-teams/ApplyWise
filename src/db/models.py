from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    value = Column(String)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)

    title = Column(String)
    company = Column(String)
    location = Column(String)
    url = Column(String, unique=True)
    source = Column(String)


class UserJob(Base):
    """
    This is the IMPORTANT table:
    - links user <-> job
    - stores when job was added for that user
    """

    __tablename__ = "user_jobs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    matched_keyword = Column(String)

    added_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "job_id"),
    )