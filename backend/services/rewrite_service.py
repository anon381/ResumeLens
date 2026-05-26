import re
from models.schemas import RewriteSuggestion

def detect_quantifiable_metrics(resume_text: str) -> int:
    """
    Finds and counts occurrences of quantifiable metrics (numbers, percentages, dollar amounts) 
    in the resume to measure bullet-point impact.
    """
    # Simple regex to find numbers, percentages, or dollar amounts
    metrics = re.findall(r'\b\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?\b', resume_text)
    return len(metrics)

def analyze_action_verbs(resume_words: list) -> list:
    """
    Checks the resume for standard high-impact action verbs.
    """
    strong_verbs_list = {
        "developed", "managed", "led", "architected", "designed", "optimized", 
        "increased", "decreased", "spearheaded", "implemented", "created", 
        "reduced", "delivered", "built"
    }
    resume_word_set = set(resume_words)
    return sorted(list(strong_verbs_list.intersection(resume_word_set)))

def generate_rewrite_suggestions(
    resume_text: str,
    resume_words: list,
    found_verbs: list,
    metrics_count: int,
    critical_missing: list,
    match_score: float
) -> dict:
    """
    Analyzes the resume text and generates personalized, actionable rewrite suggestions 
    along with examples to improve formatting, impact, and skill coverage.
    """
    suggestions = []
    rewrite_suggestions = []
    
    resume_word_set = set(resume_words)
    
    # 1. Base keywords suggestions
    if match_score < 70:
        suggestions.append("Consider adding more verbatim keywords from the job description.")
    if len(critical_missing) > 0:
        suggestions.append(f"Highlight past experience working natively with: {', '.join(critical_missing[:3])}.")
        
    # 2. Action verbs rewrite engine
    weak_verbs = {"helped", "assisted", "worked", "participated", "supported"}
    weak_found = list(weak_verbs.intersection(resume_word_set))
    strong_verbs_list = {
        "developed", "managed", "led", "architected", "designed", "optimized", 
        "increased", "decreased", "spearheaded", "implemented", "created", 
        "reduced", "delivered", "built"
    }
    
    if weak_found:
        suggestions.append("Avoid weak verbs such as: " + ", ".join(sorted(set(weak_found))) + ". Use stronger, outcome-oriented verbs instead.")
        rewrite_suggestions.append(RewriteSuggestion(
            original="Worked on machine learning model",
            improved="Developed and optimized a machine learning model achieving 92% accuracy"
        ))
        rewrite_suggestions.append(RewriteSuggestion(
            original="Helped build backend APIs",
            improved="Engineered scalable backend REST APIs returning responses 35% faster"
        ))
    elif len(found_verbs) < 3:
        missing_suggested = [v.title() for v in list(strong_verbs_list - resume_word_set)[:4]]
        suggestions.append("Add stronger action verbs to lead bullet points (examples: " + ", ".join(missing_suggested) + ").")
        rewrite_suggestions.append(RewriteSuggestion(
            original="- Built app using React",
            improved="- Designed and implemented a responsive app using React, accelerating load time by 20%"
        ))

    # 3. Quantifiable metrics suggestions
    if metrics_count == 0:
        suggestions.append("Add quantifiable metrics (numbers, %, $) to prove your impact.")
        
    return {
        "suggestions": suggestions,
        "rewrite_suggestions": rewrite_suggestions
    }
