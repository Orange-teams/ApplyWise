from pydantic import BaseModel


class Job(BaseModel):
    title: str
    company: str
    location: str
    job_format: str
    experience_level: str
    url: str
    matched_keyword: str
    source: str