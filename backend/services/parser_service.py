import io
import re
from pypdf import PdfReader

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts raw text content from PDF bytes using pypdf.
    """
    text = ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += str(extracted) + "\n"
    except Exception as e:
        print(f"Error reading PDF in parser_service: {e}")
    return text

def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Parses the upload resume file bytes depending on the file format.
    """
    text = ""
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".txt"):
        text = file_bytes.decode('utf-8', errors='ignore')
    else:
        text = file_bytes.decode('utf-8', errors='ignore')
    
    return {
        "raw_text": text,
        "entities": {"PERSON": [], "ORG": [], "GPE": []}
    }

def extract_sections(text: str) -> dict:
    """
    Extracts standard ATS sections from the resume text using regular expressions.
    """
    sections = {
        "education": "Not found",
        "experience": "Not found",
        "skills": "Not found",
        "summary": "Not found"
    }
    
    lines = text.split('\n')
    current_section = "unknown"
    section_content = {"unknown": []}
    
    # Common headers mapping
    header_map = {
        "education": r"(?i)\b(education|academic background|academic|university|degree)\b",
        "experience": r"(?i)\b(experience|work experience|employment history|professional experience|work history|career)\b",
        "skills": r"(?i)\b(skills|skill|technical skill|technical skills|core competencies|technologies|tools|expertise)\b",
        "summary": r"(?i)\b(summary|profile|professional summary|executive summary|about me|objective)\b"
    }
    
    for line in lines:
        cleaned_line = re.sub(r'[^a-zA-Z\s]', '', line.strip()).strip().lower()
        
        is_header = False
        # Headers are usually short and match our keywords
        if len(cleaned_line) > 0 and len(cleaned_line) < 40: 
            for section_key, pattern in header_map.items():
                if re.fullmatch(pattern, cleaned_line) or re.search(pattern, cleaned_line):
                    current_section = section_key
                    is_header = True
                    break
        
        if not is_header and current_section != "unknown" and line.strip():
            if current_section not in section_content:
                section_content[current_section] = []
            section_content[current_section].append(line.strip())
            
    for k in sections.keys():
        if k in section_content and len(section_content[k]) > 0:
            content_str = " \n ".join(section_content[k]).strip()
            sections[k] = content_str[:150] + "..." if len(content_str) > 150 else content_str
            
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
