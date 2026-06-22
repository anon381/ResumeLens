# ResumeLens

ResumeLens is an AI-powered resume analyzer that helps job seekers tailor their resumes to job descriptions and improve interview readiness. It combines traditional keyword/ATS checks with a TF–IDF + cosine-similarity semantic matcher to produce actionable recommendations.

<!-- Badges (replace with real URLs if desired) -->


## Overview

ResumeLens analyzes uploaded resumes (PDF/text) against a target job description and returns:

- An overall match score (hybrid keyword + semantic TF–IDF score)
- An ATS/format score to surface formatting issues
- Extracted impact metrics (quantified results detected in the resume)
- Strong action verbs used and suggestions to improve
- Targeted suggestions to increase fit for the job description

## Key Features

- Hybrid matching: semantic TF–IDF + curated keyword mappings
- Resume parsing for PDF files using a robust PDF parser
- Actionable suggestions and metrics to highlight measurable achievements
- Simple React + Vite frontend and FastAPI backend
- Ready for deployment: Render (backend) + Vercel (frontend)

## Tech Stack

- Backend: Python, FastAPI, Uvicorn, scikit-learn (TF–IDF), pypdf
- Frontend: React, Vite, Tailwind CSS
- Dev / Deployment: Render (backend), Vercel (frontend)

## Quick Start (Local Development)

Prerequisites: Python 3.9+, Node.js 18+, npm

Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend

```bash
cd frontend
npm ci
npm run dev
```
# Assignment Overview

This project serves as a machine‑learning engineering assignment, showcasing an end‑to‑end pipeline that parses resumes, extracts features, and matches them against a job description. The core ML components include:

- **Data ingestion & parsing** – PDF resumes are processed using `pypdf` to extract raw text.
- **Feature engineering** – Text is transformed into TF‑IDF vectors, enabling semantic similarity calculations.
- **Modeling** – Cosine similarity scores the semantic fit, complemented by curated keyword mappings for ATS compliance.
- **Evaluation & feedback** – The system returns a match score, ATS/format score, quantified impact metrics, and actionable suggestions to improve the resume.
- **Deployment considerations** – The backend runs as a FastAPI service inside a Python virtual environment, while the lightweight React + Vite frontend visualises results.

Run the backend and frontend as described in the Quick Start section to experience the full ML pipeline in action.



