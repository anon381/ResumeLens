# Service for extracting text from uploaded resumes.
import io
import re
from pypdf import PdfReader

def clean_pdf_text(text: str) -> str:
    """
    Cleans raw PDF text by normalizing tabs, zero-width spaces, 
    weird unicode structures, and correcting spaced-out characters.
    """
    if not text:
        return ""
    
    # 1. Standardize spacing, tabulations and newlines
    text = text.replace('\xa0', ' ').replace('\t', ' ').replace('\r', '\n')
    
    # 2. Strip out invisible zero-width unicode artifacts
    text = re.sub(r'[\u200b-\u200d\ufeff]', '', text)
    
    # 3. Correct spaced-out letters (e.g. "E x p e r i e n c e" -> "Experience")
    def merge_letters(match):
        return match.group(0).replace(' ', '')
        
    text = re.sub(r'\b[a-zA-Z0-9](?:\s[a-zA-Z0-9]){2,}\b', merge_letters, text)
    
    # 4. Collapse triple-newlines to clean spacing
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts raw text content from PDF bytes using pypdf,
    with a layout-mode fallback if text yields are extremely low.
    """
    text = ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        
        # Strategy A: Plain text extraction
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += str(extracted) + "\n"
                
        # Strategy B Fallback: Layout text extraction for complex formatting
        if len(text.strip()) < 50:
            text = ""
            for page in reader.pages:
                extracted = page.extract_text(extraction_mode="layout")
                if extracted:
                    text += str(extracted) + "\n"
                    
    except Exception as e:
        print(f"Error reading PDF in parser_service: {e}")
        
    return clean_pdf_text(text)

def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Parses the uploaded resume file bytes depending on the file format.
    """
    text = ""
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".txt"):
        text = file_bytes.decode('utf-8', errors='ignore')
    else:
        text = file_bytes.decode('utf-8', errors='ignore')
        
    # Always normalize parsed texts
    text = clean_pdf_text(text)
    
    return {
        "raw_text": text,
        "entities": {"PERSON": [], "ORG": [], "GPE": []}
    }

def extract_sections(text: str) -> dict:
    """
    Extracts standard ATS sections from the resume text using a highly robust scoring-based parser:
    1. Line-by-line clean scoring: Evaluates short lines using weighted section keywords.
    2. Character Index Partitioning Fallback: Scans raw text blocks using strict line-bounded patterns
       if any sections remain "Not found".
    """
    sections = {
        "education": "Not found",
        "experience": "Not found",
        "skills": "Not found",
        "summary": "Not found"
    }
    
    if not text.strip():
        return sections
        
    lines = text.split('\n')
    
    # We will score each short line for the 4 sections
    found_headers = []
    
    for idx, line in enumerate(lines):
        cleaned = line.strip()
        if not cleaned:
            continue
            
        # Headers are usually short (under 50 characters)
        if len(cleaned) > 50:
            continue
            
        cleaned_lower = cleaned.lower()
        
        # Clean prefix/suffix formatting (numbers, dots, bullets, hashes, spaces, colons)
        cleaned_lower = re.sub(r'^(?:[\d\.\-\#\•\*\s\–\—\|]+)', '', cleaned_lower).strip()
        cleaned_lower = re.sub(r'(?:[\s\:\-\•\*\–\—\|]+)$', '', cleaned_lower).strip()
        
        if not cleaned_lower:
            continue
            
        # Calculate weights for each section
        scores = {"education": 0, "experience": 0, "skills": 0, "summary": 0}
        
        # 1. Education Keywords
        edu_strong = [
            "education", "academic", "academics", "degree", "credential", "credentials", 
            "qualification", "qualifications", "curriculum", "scholarship", "study", "studies", 
            "diploma", "educational background", "academic credentials", "educational training"
        ]
        edu_weak = [
            "university", "college", "school", "certifications", "certification", "training", 
            "coursework", "courses", "class", "classes", "gpa", "major", "minor", "graduated"
        ]
        for kw in edu_strong:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["education"] += 10
        for kw in edu_weak:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["education"] += 5
                
        # 2. Experience Keywords
        exp_strong = [
            "experience", "employment", "career", "work history", "work experience", 
            "professional history", "career history", "employment history", "professional experience",
            "professional background", "experience record", "accomplishments", "key achievements",
            "professional development", "experience history", "work record"
        ]
        exp_weak = [
            "work", "history", "background", "professional", "development", "projects", "project", 
            "selected", "internship", "internships", "co-op", "job", "jobs", "assignments", 
            "assignment", "tenure", "position", "roles", "key projects"
        ]
        for kw in exp_strong:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["experience"] += 10
        for kw in exp_weak:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["experience"] += 5
                
        # 3. Skills Keywords
        sk_strong = [
            "skills", "skill", "technologies", "expertise", "proficiencies", "competencies", 
            "tools", "specialties", "strengths", "programming languages", "tools technologies", 
            "technical expertise", "proficiencies", "technological capabilities"
        ]
        sk_weak = [
            "technical", "abilities", "languages", "platforms", "frameworks", "technological", 
            "capabilities", "core competencies", "expertise areas"
        ]
        for kw in sk_strong:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["skills"] += 10
        for kw in sk_weak:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["skills"] += 5
                
        # 4. Summary Keywords
        sum_strong = [
            "summary", "profile", "about me", "objective", "overview", "introduction", 
            "career objective", "career summary", "professional summary", "executive summary", 
            "background summary", "mission", "personal profile"
        ]
        sum_weak = [
            "about", "personal", "executive", "mission statement", "intent", "statement"
        ]
        for kw in sum_strong:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["summary"] += 10
        for kw in sum_weak:
            if re.search(r'\b' + re.escape(kw) + r'\b', cleaned_lower):
                scores["summary"] += 5
                
        # Find highest score above minimum threshold (5)
        best_section = max(scores, key=scores.get)
        if scores[best_section] >= 5:
            # We found a match! Check if we already found this section earlier
            if not any(h[0] == best_section for h in found_headers):
                found_headers.append((best_section, idx))
                
    # If headers were successfully matched, slice the lines accordingly
    if found_headers:
        found_headers.sort(key=lambda x: x[1])
        
        for i in range(len(found_headers)):
            current_key, current_line_idx = found_headers[i]
            start_idx = current_line_idx + 1
            
            if i + 1 < len(found_headers):
                end_idx = found_headers[i + 1][1]
            else:
                end_idx = len(lines)
                
            section_lines = [l.strip() for l in lines[start_idx:end_idx] if l.strip()]
            if section_lines:
                content_str = " \n ".join(section_lines).strip()
                sections[current_key] = content_str[:150] + "..." if len(content_str) > 150 else content_str
                
    # --- FALLBACK STRATEGY: Multi-tiered Bounded/Unbounded Character Search ---
    sections_found = sum(1 for v in sections.values() if v and "Not found" not in v)
    if sections_found < 4:
        text_lower = text.lower()
        missing_keys = [k for k, v in sections.items() if "Not found" in v]
        
        fallback_indices = []
        
        # 1. Broad set of multi-word phrases (extremely safe from false-positives, even without newlines)
        fallback_phrases = {
            "education": [r"educational background", r"academic credentials", r"educational training", r"academic background"],
            "experience": [r"professional experience", r"work experience", r"employment history", r"work history", r"professional background", r"experience history", r"work record"],
            "skills": [r"programming languages", r"tools technologies", r"technical expertise", r"core competencies", r"expertise areas", r"technological capabilities"],
            "summary": [r"career objective", r"career summary", r"professional summary", r"executive summary", r"background summary", r"personal profile"]
        }
        
        # 2. Single-word keywords (require line boundaries first to ensure accuracy, else simple word boundary)
        fallback_single = {
            "education": [r"education", r"academic", r"university", r"degree"],
            "experience": [r"experience", r"employment", r"career"],
            "skills": [r"skills", r"technologies", r"expertise", r"competencies"],
            "summary": [r"summary", r"profile", r"about me", r"objective"]
        }
        
        for key in missing_keys:
            min_idx = -1
            matched_len = 0
            
            # Tier A: Match multi-word phrases at word boundaries (safe and direct)
            for pattern in fallback_phrases[key]:
                match = re.search(r'\b' + pattern + r'\b', text_lower)
                if match:
                    idx = match.start()
                    if min_idx == -1 or idx < min_idx:
                        min_idx = idx
                        matched_len = match.end() - match.start()
            
            # Tier B: Match single-word keywords strictly on line boundaries
            if min_idx == -1:
                for pattern in fallback_single[key]:
                    pattern_with_boundary = r"(?:^|\n)(?:[\s\d\.\-\#\•\*\–\—\|]*)\b" + pattern + r"\b(?:\s*[\:\-\•\*]*\s*)(?:\n|$)"
                    match = re.search(pattern_with_boundary, text_lower)
                    if match:
                        idx = match.start()
                        if min_idx == -1 or idx < min_idx:
                            min_idx = idx
                            matched_len = match.end() - match.start()
                            
            # Tier C (Absolute Last Resort): Match single-word keywords anywhere at a word boundary
            if min_idx == -1:
                for pattern in fallback_single[key]:
                    match = re.search(r'\b' + pattern + r'\b', text_lower)
                    if match:
                        idx = match.start()
                        if min_idx == -1 or idx < min_idx:
                            min_idx = idx
                            matched_len = match.end() - match.start()
                            
            if min_idx != -1:
                fallback_indices.append((key, min_idx, matched_len))
                
        if fallback_indices:
            all_indices = []
            
            # Reconstruct positions for found sections
            for key, val in sections.items():
                if "Not found" not in val:
                    content_snippet = val.replace("...", "").split(" \n ")[0]
                    idx = text.find(content_snippet)
                    if idx != -1:
                        all_indices.append((key, max(0, idx - 20), 0))
                        
            for key, idx, m_len in fallback_indices:
                all_indices.append((key, idx, m_len))
                
            all_indices.sort(key=lambda x: x[1])
            
            for i in range(len(all_indices)):
                current_key, current_start, m_len = all_indices[i]
                if current_key in missing_keys:
                    content_start = current_start + m_len
                    if i + 1 < len(all_indices):
                        content_end = all_indices[i + 1][1]
                    else:
                        content_end = len(text)
                        
                    content = text[content_start:content_end].strip()
                    if content:
                        content = re.sub(r'^[\s\:\-\•\*\-\–\—\|]+', '', content).strip()
                        sections[current_key] = content[:150] + "..." if len(content) > 150 else content
                        
    return sections

def classify_role(text: str) -> str:
    """
    Classifies the resume role based on the frequency of specific keywords.
    """
    text_lower = text.lower()
    roles = {
        "Software Engineer": ["software", "developer", "programmer", "engineer", "full stack", "frontend", "backend"],
        "Data Scientist": ["data science", "machine learning", "analytics", "data analyst", "deep learning"],
        "Product Manager": ["product manager", "project manager", "scrum", "agile", "pmp"],
        "UI/UX Designer": ["ui/ux", "designer", "figma", "user experience", "user interface"]
    }
    scores = {role: sum(1 for k in keywords if k in text_lower) for role, keywords in roles.items()}
    best_role = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else "General Professional"
    return best_role
