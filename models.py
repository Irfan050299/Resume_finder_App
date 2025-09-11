from pydantic import BaseModel
from typing import List

# Resume extraction model
class ResumeModel(BaseModel):
    name: str
    email: str
    phone: int
    skills: List[str]
    year_of_exp: int

# Recruiter final description
class RecruiterDesc(BaseModel):
    Candidate: str
    experience: int
    skills: List[str]
    EngDesc: str
    SpanishDes: str
