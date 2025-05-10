from pydantic import BaseModel
from typing import List, Optional

class CandidateProfile(BaseModel):
    name: str
    education: List[str]
    experience: List[str]
    skills: List[str]
    certifications: List[str]
    projects: List[str]
    web_links: dict

class FitResult(BaseModel):
    fit_score: str
    profile: CandidateProfile
    comparison_matrix: dict
    explanation: str