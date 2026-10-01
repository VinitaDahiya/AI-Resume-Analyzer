from pydantic import BaseModel
from typing import List


class RequirementAnalysis(BaseModel):
    requirement: str
    status: str
    evidence: str


class ResumeAnalysis(BaseModel):
    requirement_analysis: List[RequirementAnalysis]
    relevant_experience: List[str]
    experience_gaps: List[str]
    strengths: List[str]
    gaps: List[str]
    overall_assessment: str