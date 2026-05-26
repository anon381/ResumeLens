from models.schemas import ScoreBreakdown

def calculate_scoring_breakdown(
    ats_score: float,          # out of 100
    semantic_match: float,      # out of 100
    skill_coverage: float,      # out of 100
    metrics_count: int,
    found_verbs_count: int,
    formatting_score: float
) -> tuple:
    """
    Computes a hybrid weighted match score and compiles a ScoreBreakdown.
    The breakdown architecture is:
      - ATS Compatibility: 20%
      - Semantic Match: 30%
      - Skill Coverage: 20%
      - Impact Metrics: 15% (scaled by quantity up to 5 metrics)
      - Experience Quality: 15% (scaled by action verb quantity up to 5)
    """
    # Components weights
    ats_component = (ats_score / 100.0) * 20.0
    semantic_component = (semantic_match / 100.0) * 30.0
    keyword_component = (skill_coverage / 100.0) * 20.0
    
    # Impact component (15% max, capped at 5 metrics)
    impact_component = min((metrics_count / 5.0) * 15.0, 15.0)
    
    # Experience Quality component (15% max, capped at 5 verbs)
    verb_component = min((found_verbs_count / 5.0) * 15.0, 15.0)
    
    # Sum the weighted components
    match_score = round(ats_component + semantic_component + keyword_component + impact_component + verb_component, 2)
    match_score = min(max(match_score, 0.0), 100.0)
    
    # Compile ScoreBreakdown (representing out of 100 for each aspect)
    score_breakdown = ScoreBreakdown(
        ats_compatibility=round(ats_score, 2),
        semantic_match=round(semantic_match, 2),
        skill_coverage=round(skill_coverage, 2),
        impact_metrics=round(impact_component * (100.0 / 15.0), 2),
        experience_quality=round(verb_component * (100.0 / 15.0), 2),
        formatting=formatting_score
    )
    
    return match_score, score_breakdown

def generate_recruiter_summary(match_score: float) -> str:
    """
    Generates a high-level recruiter summary depending on the overall match score.
    """
    if match_score >= 80:
        return "🔥 Top Tier Candidate. Extremely high keyword alignment with the job description. Recommend immediate screening."
    elif match_score >= 60:
        return "✅ Solid Fit. Candidate possesses core competencies but may require upskilling in a few niche requirements."
    else:
        return "⚠️ Potential Risk. Resume lacks significant overlap with critical job requirements. Proceed with caution."
