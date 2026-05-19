from pydantic import BaseModel


class CVEditPolicy(BaseModel):
    summary: bool
    experience: bool
    skills: bool
    education: bool
    projects: bool
    publications: bool