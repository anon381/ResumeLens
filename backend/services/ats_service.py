from models.schemas import MatchResult
from services.parser_service import extract_sections, classify_role
from services.skill_service import extract_keywords, extract_explicit_skills, analyze_skills_overlap
from services.semantic_service import calculate_semantic_similarity
from services.rewrite_service import detect_quantifiable_metrics, analyze_action_verbs, generate_rewrite_suggestions
from services.scoring_service import calculate_scoring_breakdown, generate_recruiter_summary

def check_ats_compatibility(resume_text: str, sections: dict) -> dict:
    """
    Analyzes structural features of the resume (like presence of core sections,
    formatting quality, and overall parser readability) to determine an ATS Compatibility score.
    """
    # Count sections found (Education, Experience, Skills, Summary)
    sections_found = sum(1 for v in sections.values() if v and "Not found" not in v)
    
    # Base ATS compatibility out of 100
    ats_score = (sections_found / 4.0) * 100.0
    
    # Determine formatting score
    formatting_score = 100.0 if sections_found > 0 else 50.0
    
    # Identify structure suggestions
    structure_suggestions = []
    missing_sections = [k.title() for k, v in sections.items() if not v or "Not found" in v]
    if missing_sections:
        structure_suggestions.append(f"Add the following standard ATS sections: {', '.join(missing_sections)}.")
        
    return {
        "ats_score": ats_score,
        "sections_found_count": sections_found,
        "formatting_score": formatting_score,
        "suggestions": structure_suggestions
    }

def calculate_match(resume_text: str, jd_text: str) -> MatchResult:
    """
    The main orchestration engine of the ATS application. Uses specialized sub-services
    to build a comprehensive profile, similarity breakdown, and recommendation report.
    """
    # 1. Parse & extract structure, role classification
    sections = extract_sections(resume_text)
    role_classification = classify_role(resume_text)
    
    # 2. Analyze skills and keyword overlap
    skills_analysis = analyze_skills_overlap(resume_text, jd_text)
    matched_skills = skills_analysis["matched_skills"]
    critical_missing = skills_analysis["critical_missing"]
    nice_to_have = skills_analysis["nice_to_have"]
    skill_coverage_score = skills_analysis["base_score"]
    
    # 3. Calculate semantic cosine similarity
    semantic_match_score = calculate_semantic_similarity(resume_text, jd_text)
    
    # 4. Check ATS compatibility
    ats_analysis = check_ats_compatibility(resume_text, sections)
    ats_score = ats_analysis["ats_score"]
    formatting_score = ats_analysis["formatting_score"]
    structure_suggestions = ats_analysis["suggestions"]
    
    # 5. Extract metrics & action verbs
    resume_words = extract_keywords(resume_text)
    metrics_count = detect_quantifiable_metrics(resume_text)
    found_verbs = analyze_action_verbs(resume_words)
    
    # 6. Calculate scoring breakdown
    match_score, score_breakdown = calculate_scoring_breakdown(
        ats_score=ats_score,
        semantic_match=semantic_match_score,
        skill_coverage=skill_coverage_score,
        metrics_count=metrics_count,
        found_verbs_count=len(found_verbs),
        formatting_score=formatting_score
    )
    
    # 7. Generate improvement suggestions & rewrite examples
    suggestions_analysis = generate_rewrite_suggestions(
        resume_text=resume_text,
        resume_words=resume_words,
        found_verbs=found_verbs,
        metrics_count=metrics_count,
        critical_missing=critical_missing,
        match_score=match_score
    )
    suggestions = suggestions_analysis["suggestions"] + structure_suggestions
    rewrite_suggestions = suggestions_analysis["rewrite_suggestions"]
    
    # 8. Generate high-level recruiter insights
    recruiter_summary = generate_recruiter_summary(match_score)
    
    # 9. Extract pre-defined explicit skills
    explicit_skills = extract_explicit_skills(resume_text)
    
    # Floor score adjustment (UX enhancement for non-zero overlap)
    if match_score == 0.0 and resume_text.strip() and jd_text.strip():
        match_score = 5.0

    return MatchResult(
        match_score=match_score,
        score_breakdown=score_breakdown,
        matched_skills=matched_skills[:12],
        missing_critical_skills=critical_missing[:6],
        missing_nice_to_have_skills=nice_to_have[:6],
        suggestions=suggestions,
        rewrite_suggestions=rewrite_suggestions,
        recruiter_summary=recruiter_summary,
        quantifiable_metrics_count=metrics_count,
        strong_action_verbs=found_verbs[:5],
        extracted_sections=sections,
        extracted_skills=explicit_skills,
        role_classification=role_classification
    )
