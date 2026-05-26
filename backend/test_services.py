import os
from services.parser_service import parse_resume, extract_sections, classify_role
from services.semantic_service import calculate_semantic_similarity
from services.skill_service import extract_keywords, extract_explicit_skills, analyze_skills_overlap
from services.rewrite_service import detect_quantifiable_metrics, analyze_action_verbs, generate_rewrite_suggestions
from services.scoring_service import calculate_scoring_breakdown, generate_recruiter_summary
from services.ats_service import calculate_match, check_ats_compatibility
from services.ranking_service import rank_resumes

def main():
    print("=== STARTING MODULAR SERVICES UNIT TESTS ===")
    
    # 1. Load sample files
    resume_path = "../sample_resume.txt"
    jd_path = "../sample_jd.txt"
    
    if not os.path.exists(resume_path) or not os.path.exists(jd_path):
        print("❌ Error: Sample files not found at root!")
        return
        
    with open(resume_path, "r") as f:
        resume_text = f.read()
    with open(jd_path, "r") as f:
        jd_text = f.read()
        
    print(f"Loaded Resume ({len(resume_text)} chars) and Job Description ({len(jd_text)} chars).")
    
    # 2. Test Parser Service
    print("\n--- 1. Testing parser_service ---")
    sections = extract_sections(resume_text)
    role = classify_role(resume_text)
    print(f"✓ Sections Extracted: {list(sections.keys())}")
    print(f"✓ Role Classified: {role}")
    
    # 3. Test Skill Service
    print("\n--- 2. Testing skill_service ---")
    explicit = extract_explicit_skills(resume_text)
    keywords = extract_keywords(resume_text)
    overlap = analyze_skills_overlap(resume_text, jd_text)
    print(f"✓ Explicit Skills Found: {explicit}")
    print(f"✓ Total Unique Keywords Found: {len(keywords)}")
    print(f"✓ Skills Overlap Score: {overlap['base_score']}%")
    print(f"✓ Matched Skills: {overlap['matched_skills'][:5]}")
    print(f"✓ Critical Missing: {overlap['critical_missing'][:5]}")
    
    # 4. Test Semantic Service
    print("\n--- 3. Testing semantic_service ---")
    sem_similarity = calculate_semantic_similarity(resume_text, jd_text)
    print(f"✓ Semantic Similarity Score: {sem_similarity}%")
    
    # 5. Test Rewrite Service
    print("\n--- 4. Testing rewrite_service ---")
    metrics_count = detect_quantifiable_metrics(resume_text)
    verbs = analyze_action_verbs(keywords)
    rewrites = generate_rewrite_suggestions(
        resume_text=resume_text,
        resume_words=keywords,
        found_verbs=verbs,
        metrics_count=metrics_count,
        critical_missing=overlap["critical_missing"],
        match_score=75.0
    )
    print(f"✓ Quantifiable Metrics Count: {metrics_count}")
    print(f"✓ Action Verbs Found: {verbs}")
    print(f"✓ Rewrite Suggestions Count: {len(rewrites['rewrite_suggestions'])}")
    
    # 6. Test Scoring Service
    print("\n--- 5. Testing scoring_service ---")
    overall, breakdown = calculate_scoring_breakdown(
        ats_score=80.0,
        semantic_match=sem_similarity,
        skill_coverage=overlap["base_score"],
        metrics_count=metrics_count,
        found_verbs_count=len(verbs),
        formatting_score=100.0
    )
    recruiter_msg = generate_recruiter_summary(overall)
    print(f"✓ Calculated Match Score: {overall}%")
    print(f"✓ Score Breakdown: {breakdown}")
    print(f"✓ Recruiter Summary: {recruiter_msg}")
    
    # 7. Test ATS Service (Orchestrator)
    print("\n--- 6. Testing ats_service (Main Orchestrator) ---")
    match_result = calculate_match(resume_text, jd_text)
    print(f"✓ Orchestrated Match Score: {match_result.match_score}%")
    print(f"✓ Orchestrated Score Breakdown: {match_result.score_breakdown}")
    
    # 8. Test Ranking Service
    print("\n--- 7. Testing ranking_service ---")
    candidates = [
        {"name": "Alice Developer", "resume_text": resume_text},
        {"name": "Bob Empty", "resume_text": ""},
        {"name": "Charlie Minimal", "resume_text": "I am a Software Developer. I do Python and React."}
    ]
    ranked = rank_resumes(candidates, jd_text)
    print("✓ Candidates Ranked:")
    for idx, candidate in enumerate(ranked):
        print(f"  [{idx + 1}] {candidate['name']} - Score: {candidate['match_score']}% (Role: {candidate['role_classification']})")
        
    print("\n=== ALL SERVICES UNIT TESTS COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
