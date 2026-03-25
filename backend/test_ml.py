from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

print("=== 1. Starting AI/ML Setup Test (Scikit-Learn) ===")

# Paths to samples
resume_path = "../sample_resume.txt"
jd_path = "../sample_jd.txt"

if not os.path.exists(resume_path) or not os.path.exists(jd_path):
    print("Sample texts not found. Please ensure sample_resume.txt and sample_jd.txt exist.")
    exit()

with open(resume_path, "r") as f:
    resume = f.read()

with open(jd_path, "r") as f:
    jd = f.read()

print("Using TF-IDF Vectorizer from Scikit-Learn...")

print("\n=== 2. Testing Semantic Match (TF-IDF Cosine Similarity) ===")
try:
    vectorizer = TfidfVectorizer(stop_words='english')
    # Fit and transform the texts
    tfidf_matrix = vectorizer.fit_transform([jd, resume])
    
    # Calculate Cosine Similarity between JD (index 0) and Resume (index 1)
    cosine_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    print(f"-> Semantic Match Similarity Score: {cosine_score * 100:.2f}%")
    
    print("\nTop Matching Keywords Extract:")
    feature_names = vectorizer.get_feature_names_out()
    # Get highest TF-IDF scores for the resume
    resume_vector = tfidf_matrix[1:2].T.todense()
    # Sort and get top 5
    import numpy as np
    top_indices = np.argsort(resume_vector, axis=0)[-5:]
    for idx in reversed(top_indices):
        print(f"  - {feature_names[idx.item()]}")

except Exception as e:
    print(f"Similarity error: {e}")

print("\n=== Test Complete ===")
