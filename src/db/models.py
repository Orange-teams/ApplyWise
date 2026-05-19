from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Text
from datetime import datetime

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    added_at = Column(DateTime, default=datetime.utcnow)


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
    job_description = Column(Text)


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

class TailoredResume(Base):
    __tablename__ = "tailored_resumes"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    model_name = Column(String)
    template_name = Column(String)
    tex_path = Column(String)
    pdf_path = Column(String)
    status = Column(String)
    created_at = Column(DateTime)