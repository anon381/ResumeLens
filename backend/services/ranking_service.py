from typing import List, Dict, Any
from services.ats_service import calculate_match

def rank_resumes(candidates: List[Dict[str, Any]], jd_text: str) -> List[Dict[str, Any]]:
    """
    Compares and ranks a collection of resumes against a target job description.
    
    Each candidate dictionary must provide:
      - 'name' or 'id': identifier for the candidate
      - 'resume_text': raw text string of the resume content
      
    Returns the list of candidates enriched with match scoring details, sorted
    in descending order of compatibility.
    """
    ranked_results = []
    
    for candidate in candidates:
        name = candidate.get("name", candidate.get("id", "Unnamed Candidate"))
        resume_text = candidate.get("resume_text", "")
        
        if not resume_text.strip():
            ranked_results.append({
                "name": name,
                "match_score": 0.0,
                "role_classification": "N/A (Empty Resume)",
                "recruiter_summary": "Empty resume provided.",
                "matched_skills": [],
                "missing_skills": []
            })
            continue
            
        try:
            match_result = calculate_match(resume_text, jd_text)
            ranked_results.append({
                "name": name,
                "match_score": match_result.match_score,
                "role_classification": match_result.role_classification,
                "score_breakdown": {
                    "ats_compatibility": match_result.score_breakdown.ats_compatibility,
                    "semantic_match": match_result.score_breakdown.semantic_match,
                    "skill_coverage": match_result.score_breakdown.skill_coverage,
                    "impact_metrics": match_result.score_breakdown.impact_metrics,
                    "experience_quality": match_result.score_breakdown.experience_quality,
                    "formatting": match_result.score_breakdown.formatting
                },
                "recruiter_summary": match_result.recruiter_summary,
                "matched_skills": match_result.matched_skills,
                "missing_skills": match_result.missing_critical_skills
            })
        except Exception as e:
            print(f"Error evaluating candidate '{name}' in ranking_service: {e}")
            ranked_results.append({
                "name": name,
                "match_score": 0.0,
                "role_classification": "Parsing Error",
                "recruiter_summary": f"Failed to analyze: {str(e)}",
                "matched_skills": [],
                "missing_skills": []
            })
            
    # Sort descending by match_score
    ranked_results.sort(key=lambda x: x["match_score"], reverse=True)
    
    return ranked_results
