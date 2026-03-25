from pypdf import PdfReader
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    text = ""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += str(extracted) + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def parse_resume(file_bytes: bytes, filename: str):
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
