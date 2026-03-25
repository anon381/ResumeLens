from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from models.schemas import MatchResult, JobDescriptionInput
from services.parser import parse_resume
from services.matcher import calculate_match

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported")
    
    content = await file.read()
    parsed_data = parse_resume(content, file.filename)
    
    return {"message": "Resume parsed successfully", "data": parsed_data}

@router.post("/analyze", response_model=MatchResult)
async def analyze_resume(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    try:
        result = calculate_match(resume_text, job_description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
