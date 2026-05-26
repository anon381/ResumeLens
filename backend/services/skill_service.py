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
    Extracts highly relevant professional, technical, and domain-specific skills and concepts 
    from the text, filtering out generic verbs, adjectives, and job-posting noise.
    """
    # 1. Clean the text and extract word tokens (including special chars like c++, c#, next.js)
    words = re.findall(r'\b[A-Za-z0-9_\-\.\#\+]+', text.lower())
    
    # 2. Comprehensive dictionary of real skill taxonomy (technical, professional, and methodologies)
    skill_taxonomy = {
        # Programming & Scripting
        "python", "javascript", "typescript", "java", "c++", "c#", "ruby", "go", "golang", "rust", 
        "swift", "kotlin", "php", "sql", "r", "scala", "perl", "bash", "shell", "html", "css", "sass", 
        "less", "graphql", "markdown",
        
        # Frameworks, Libraries & Frontend
        "react", "angular", "vue", "next.js", "nextjs", "nuxt", "svelte", "node.js", "nodejs", 
        "express", "expressjs", "nest.js", "nestjs", "django", "fastapi", "flask", "spring", 
        "spring boot", "springboot", "laravel", "rails", "asp.net", "net core", "bootstrap", 
        "tailwind", "tailwindcss", "pytorch", "tensorflow", "scikit-learn", "scikit", "pandas", 
        "numpy", "keras", "opencv", "nltk", "spacy", "huggingface", "transformers", "transformer",
        "vite", "webpack", "redux", "jquery", "ajax",
        
        # Databases & Cache
        "mysql", "postgresql", "postgres", "sqlite", "oracle", "sql server", "mongodb", "redis", 
        "elasticsearch", "cassandra", "dynamodb", "neo4j", "mariadb", "firebase", "supabase", 
        "prisma", "hibernate", "couchdb", "memcached",
        
        # Cloud, DevOps & Infrastructure
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "terraform", "ansible", 
        "jenkins", "git", "github", "gitlab", "ci/cd", "cicd", "nginx", "apache", "linux", "unix", 
        "vagrant", "prometheus", "grafana", "cloudformation", "lambda", "ecs", "s3", "ec2", "rds",
        "kubernetes orchestration", "dockerization",
        
        # AI, ML, NLP & Data Science
        "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", 
        "ai", "artificial intelligence", "data science", "data analysis", "statistics", "regression", 
        "classification", "clustering", "neural networks", "llm", "large language models", "bert", 
        "gpt", "data visualization", "tableau", "power bi", "etl", "spark", "hadoop", "kafka", 
        "data warehousing", "preprocessing", "tokenization", "embeddings", "embedding", 
        "finetuning", "fine-tuning", "dimensionality reduction", "pca", "kmeans", "random forest", 
        "xgboost", "milvus", "pinecone", "chromadb", "vector databases", "predictive modeling",
        
        # Methodologies & Architecture
        "agile", "scrum", "kanban", "devops", "oop", "object-oriented programming", "functional programming", 
        "rest", "restful", "api", "apis", "microservices", "system design", "architecture", "mvc", 
        "tdd", "test-driven development", "ci", "cd", "clean code", "solid principles", "design patterns", 
        "qa", "testing", "debugging", "cloud computing", "web development", "mobile development", 
        "version control", "software engineering", "sdlc",
        
        # Design & Product
        "figma", "sketch", "adobe xd", "photoshop", "illustrator", "ui", "ux", "user interface", 
        "user experience", "wireframing", "prototyping", "product management", "project management", 
        "product strategy", "scrum master", "pmp", "jira", "confluence", "trello", "asana",
        
        # Domains & Domains
        "finance", "marketing", "sales", "accounting", "seo", "saas", "b2b", "b2c", "cybersecurity", 
        "security", "cryptography", "blockchain", "networking", "devsecops", "saas architecture",
        
        # Professional/Soft Skills (Cleaned)
        "collaboration", "collaborating", "communication", "leadership", "teamwork", "coaching", 
        "mentoring", "negotiation", "adaptability", "problem-solving", "critical thinking"
    }
    
    # 3. List of generic words to filter out (adjectives, verbs, and filler job description text)
    generic_noise = {
        "looking", "nice", "have", "required", "preferred", "least", "years", "experience", 
        "candidate", "role", "team", "building", "using", "powered", "prioritized", "understanding", 
        "teams", "modern", "include", "candidates", "analyzing", "preprocessing", "collaborating", 
        "solid", "strong", "excellent", "outstanding", "great", "proven", "successful", "passionate", 
        "talented", "motivated", "dynamic", "ideal", "additional", "basic", "advanced", "key", 
        "core", "develop", "developing", "build", "create", "creating", "implement", "implementing", 
        "design", "designing", "manage", "managing", "lead", "leading", "support", "supporting", 
        "deliver", "delivering", "work", "working", "drive", "driving", "ensure", "ensuring", 
        "optimize", "optimizing", "company", "business", "product", "products", "service", "services", 
        "user", "users", "customer", "customers", "client", "clients", "requirements", "qualifications", 
        "skills", "ability", "abilities", "join", "help", "highly", "growth", "high", "fast-paced",
        "industry", "solutions", "systems", "processes", "workflows", "practices", "best", "quality",
        "standards", "world", "class", "innovative", "impact", "results", "value", "goals", "missions",
        "objectives", "requirements", "needs", "responsibilities", "duties", "tasks", "activities"
    }
    
    # Clean up and normalize
    cleaned_words = []
    for w in words:
        # Strip trailing/leading punctuation
        w_clean = w.strip('.-+#').lower()
        if not w_clean or len(w_clean) < 3:
            continue
            
        # Ignore numeric strings (like year counts)
        if w_clean.isdigit():
            continue
            
        # If it is a known stopword or noise word, skip it
        if w_clean in STOP_WORDS or w_clean in generic_noise:
            continue
            
        cleaned_words.append(w_clean)
        
    # Filter: we prefer words that belong to the taxonomy, or are specific technical/industry terms
    final_keywords = []
    for w in cleaned_words:
        if w in skill_taxonomy:
            final_keywords.append(w)
        elif any(c in w for c in ['+', '#', '.', '-']):
            final_keywords.append(w)
        elif len(w) >= 4 and w not in generic_noise:
            final_keywords.append(w)
            
    # Deduplicate while preserving order
    seen = set()
    ordered_unique = []
    for kw in final_keywords:
        if kw not in seen:
            seen.add(kw)
            ordered_unique.append(kw)
            
    return ordered_unique

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
