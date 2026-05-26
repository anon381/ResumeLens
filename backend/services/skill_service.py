import re

STOP_WORDS = set([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "about", 
    "as", "into", "like", "through", "after", "over", "between", "out", "against", "during", 
    "without", "before", "under", "around", "among", "of", "from", "is", "are", "was", "were", 
    "be", "been", "being", "have", "has", "had", "do", "does", "did", "can", "could", "will", 
    "would", "should", "shall", "may", "might", "must", "it", "its", "they", "them", "their", 
    "he", "him", "his", "she", "her", "we", "us", "our", "you", "your", "i", "me", "my", 
    "this", "that", "these", "those", "not", "no"
])

def extract_explicit_skills(text: str) -> list:
    """
    Extracts pre-defined common technology/skill keywords present in the text.
    """
    common_skills = {
        "python", "java", "c++", "c#", "javascript", "typescript", "react", "angular", "vue", 
        "node.js", "django", "fastapi", "flask", "spring", "aws", "azure", "gcp", "docker", 
        "kubernetes", "sql", "mysql", "postgresql", "mongodb", "html", "css", "machine learning", 
        "data science", "tensorflow", "pytorch"
    }
    text_lower = text.lower()
    return [s for s in common_skills if s in text_lower]

def extract_keywords(text: str) -> list:
    """
    Cleans text, filters standard stopwords and generic JD noise,
    and returns unique candidate words/skills.
    """
    words = re.findall(r'\b[A-Za-z0-9_]+\b', text.lower())
    # Exclude strict stopwords and generic job description noise
    jd_noise = {
        "looking", "nice", "have", "required", "preferred", "least", "years", 
        "experience", "candidate", "role", "team", "building", "using"
    }
    return [w for w in words if w not in STOP_WORDS and w not in jd_noise and len(w) > 2]

def analyze_skills_overlap(resume_text: str, jd_text: str) -> dict:
    """
    Compares keywords between resume and job description to find matched skills, 
    missing critical skills, missing nice-to-have skills, and calculates a base overlap percentage score.
    """
    resume_words = extract_keywords(resume_text)
    jd_words = extract_keywords(jd_text)
    
    resume_skills = set(resume_words)
    jd_skills = set(jd_words)
    
    matched_skills = list(resume_skills.intersection(jd_skills))
    missing_skills = list(jd_skills - resume_skills)
    
    total_jd_words = len(jd_skills)
    if total_jd_words == 0:
        base_score = 100.0
    else:
        base_score = round((len(matched_skills) / total_jd_words) * 100, 2)
        
    critical_missing = missing_skills[:max(1, len(missing_skills)//3)]
    nice_to_have = missing_skills[max(1, len(missing_skills)//3):]
    
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "critical_missing": critical_missing,
        "nice_to_have": nice_to_have,
        "base_score": base_score
    }
