# ResumeLens

ResumeLens is an AI-powered resume analyzer that helps job seekers tailor their resumes to job descriptions and improve interview readiness. It combines traditional keyword/ATS checks with a TF–IDF + cosine-similarity semantic matcher to produce actionable recommendations.

<!-- Badges (replace with real URLs if desired) -->

- Build: ![build badge](https://img.shields.io/badge/build-passing-brightgreen)
- License: ![license badge](https://img.shields.io/badge/license-MIT-blue)

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

Open the frontend at http://localhost:5173 and confirm the API URL points to the backend (use `VITE_API_URL` env var if needed).

## Deployment

Deployment recommendations and step-by-step instructions are included in [DEPLOY.md](DEPLOY.md).

## Contributing

Contributions are welcome. Open an issue to propose changes or submit a pull request with a clear description and tests where applicable.

## License

This project is available under the MIT License. See the `LICENSE` file for details.

## Contact

If you need help or want this project adapted for a specific role or pipeline, open an issue or contact the maintainer.
