from sqlalchemy import Column, Integer, JSON, String, ForeignKey, DateTime, UniqueConstraint, Text
from src.utils.time import now
from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    added_at = Column(DateTime, default=now)


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
    __tablename__ = "user_jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    matched_keyword = Column(String)
    created_at = Column(DateTime, default=now)

    __table_args__ = (
        UniqueConstraint("user_id", "job_id"),
    )

class UserCV(Base):
    __tablename__ = "user_cvs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    raw_latex = Column(Text)          # original input
    parsed_json = Column(JSON)        # structured CV (IMPORTANT)
    cv_edit_policy = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=now)

class TailoredCV(Base):
    __tablename__ = "tailored_cvs"

    id = Column(Integer, primary_key=True)
    user_cv_id = Column(Integer, ForeignKey("user_cvs.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    edited_json = Column(JSON)     # LLM output (structured)
    final_latex = Column(Text)     # rendered LaTeX
    pdf_path = Column(String)
    created_at = Column(DateTime, default=now)