from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculates TF-IDF cosine similarity between the resume text and the job description,
    returning a percentage match score normalized out of 100.
    """
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        cosine_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Translate the cosine decimal (0.0 to 1.0) into a percentage
        # We give it a generous bump because perfect 1.0 is hard to achieve with natural resumes
        ai_match_score = min(round((cosine_score * 100) * 1.5, 2), 100.0) 
    except Exception as e:
        print(f"Error calculating semantic similarity: {e}")
        ai_match_score = 0.0
        
    return ai_match_score
