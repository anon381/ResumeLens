from pydantic import BaseModel
from typing import List, Dict

class JobDescriptionInput(BaseModel):
    text: str

class RewriteSuggestion(BaseModel):
    original: str
    improved: str

class ScoreBreakdown(BaseModel):
    ats_compatibility: float
    semantic_match: float
    skill_coverage: float
    impact_metrics: float
    experience_quality: float
    formatting: float

class MatchResult(BaseModel):
    match_score: float
    score_breakdown: ScoreBreakdown
    ats_score: float
    matched_skills: List[str]
    missing_critical_skills: List[str]
    missing_nice_to_have_skills: List[str]
    suggestions: List[str]
    rewrite_suggestions: List[RewriteSuggestion]
    recruiter_summary: str
    quantifiable_metrics_count: int
    strong_action_verbs: List[str]
    extracted_sections: dict
    extracted_skills: List[str]
    role_classification: str
