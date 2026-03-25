import re
from models.schemas import MatchResult
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

STOP_WORDS = set(["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "about", "as", "into", "like", "through", "after", "over", "between", "out", "against", "during", "without", "before", "under", "around", "among", "of", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "can", "could", "will", "would", "should", "shall", "may", "might", "must", "it", "its", "they", "them", "their", "he", "him", "his", "she", "her", "we", "us", "our", "you", "your", "i", "me", "my", "this", "that", "these", "those", "will", "can", "not", "no"])

def extract_keywords(text: str):
    words = re.findall(r'\b[A-Za-z0-9_]+\b', text.lower())
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]

def calculate_match(resume_text: str, jd_text: str) -> MatchResult:
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(jd_text)
    
    resume_skills = set(resume_words)
    jd_skills = set(jd_words)
    
    matched_skills = list(resume_skills.intersection(jd_skills))
    missing_skills = list(jd_skills - resume_skills)
    
    # --- AI/ML UPGRADE: TF-IDF Cosine Similarity ---
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        cosine_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Translate the cosine decimal (0.0 to 1.0) into a percentage
        # We give it a generous bump because perfect 1.0 is impossible for real resumes
        ai_match_score = min(round((cosine_score * 100) * 1.5, 2), 100.0) 
    except Exception:
        # Fallback to basic word math if ML fails
        ai_match_score = 0.0

    total_jd_words = len(jd_skills)
    if total_jd_words == 0:
        base_score = 100.0
    else:
        base_score = round((len(matched_skills) / total_jd_words) * 100, 2)
        
    # Hybrid Score: Combine TF-IDF ML Vector base with exact Keyword matching
    match_score = round((ai_match_score * 0.6) + (base_score * 0.4), 2)
    match_score = min(max(match_score, 0.0), 100.0)
    
    if match_score < 70 and len(matched_skills) > 10:
        match_score += 15
        match_score = min(match_score, 100.0)
        
    critical_missing = missing_skills[:max(1, len(missing_skills)//3)]
    nice_to_have = missing_skills[max(1, len(missing_skills)//3):]
    
    suggestions = []
    if match_score < 70:
        suggestions.append("Consider adding more verbatim keywords from the job description.")
    if len(critical_missing) > 0:
        suggestions.append(f"Highlight past experience working natively with: {', '.join(critical_missing[:3])}.")
    suggestions.append("Ensure your action verbs match the seniority of the role (e.g. 'Architected' vs 'Helped build').")
        
    # Recruiter-specific insights
    if match_score >= 80:
        recruiter_summary = "🔥 Top Tier Candidate. Extremely high keyword alignment with the job description. Recommend immediate screening."
    elif match_score >= 60:
        recruiter_summary = "✅ Solid Fit. Candidate possesses core competencies but may require upskilling in a few niche requirements."
    else:
        recruiter_summary = "⚠️ Potential Risk. Resume lacks significant overlap with critical job requirements. Proceed with caution."

    # Simulated market trends based on jd skills
    tech_trends = ["Kubernetes", "GraphQL", "TypeScript", "CI/CD", "TailwindCSS", "AWS Lambdas"]
    market_trends = [t for t in tech_trends if t.lower() not in resume_words][:3]
    if not market_trends:
        market_trends = ["No immediate trend warnings."]

    # NEW FEATURE: Resume Impact Analysis (Action Verbs and Metrics)
    strong_verbs_list = {"developed", "managed", "led", "architected", "designed", "optimized", "increased", "decreased", "spearheaded", "implemented", "created", "reduced", "delivered", "built"}
    found_verbs = list(strong_verbs_list.intersection(set(resume_text.lower().split())))
    
    # Simple regex to find quantifiable metrics (numbers, percentages, dollar amounts)
    metrics = re.findall(r'\b\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?\b', resume_text)
    metrics_count = len(metrics)

    if metrics_count == 0:
        suggestions.append("Add quantifiable metrics (numbers, %, $) to prove your impact.")
    if len(found_verbs) < 3:
        suggestions.append("Use more strong action verbs (e.g., 'Architected', 'Optimized') to start your bullet points.")

    return MatchResult(
        match_score=match_score,
        matched_skills=matched_skills[:12],
        missing_critical_skills=critical_missing[:6],
        missing_nice_to_have_skills=nice_to_have[:6],
        suggestions=suggestions,
        ats_score=min(100.0, match_score + 15),
        recruiter_summary=recruiter_summary,
        market_trends=market_trends,
        quantifiable_metrics_count=metrics_count,
        strong_action_verbs=found_verbs[:5]
    )
