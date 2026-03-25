from pydantic import BaseModel
from typing import List

class JobDescriptionInput(BaseModel):
    text: str

class MatchResult(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_critical_skills: List[str]
    missing_nice_to_have_skills: List[str]
    suggestions: List[str]
    ats_score: float
    recruiter_summary: str
    market_trends: List[str]
    quantifiable_metrics_count: int
    strong_action_verbs: List[str]
