Quick recommended deployment

Overview

- Backend: Render (Python web service)
- Frontend: Vercel (static React app built with Vite)

Files added

- `backend/requirements.txt` — Python deps for Render
- `backend/Procfile` — start command for Render

Backend (Render) — steps

1. Push your repo to GitHub (or connect your Git provider to Render).
2. In Render, create a new **Web Service**.
   - Repository: select this repo
   - Root directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables if needed (e.g., `ALLOWED_ORIGINS`, model keys).
4. Render will build and expose a public URL (e.g., `https://your-backend.onrender.com`).
5. Update frontend to call the deployed backend URL (or set an env var in Vercel).

Frontend (Vercel) — steps

1. Push your repo to GitHub.
2. In Vercel, create a new project and import the frontend folder.
   - Framework Preset: `Vite` / `Other` (Vite will be detected)
   - Root Directory: `frontend`
   - Build Command: `npm run build` (already in `package.json`)
   - Output Directory: `dist`
3. Set an environment variable `VITE_API_URL` (or update `src/services/api.js` to read from env) with your Render backend URL (e.g., `https://your-backend.onrender.com/api`).
4. Deploy — Vercel will provide a public URL (e.g., `https://your-frontend.vercel.app`).

CORS

- The backend `main.py` currently allows all origins. For production, limit `allow_origins` to your Vercel URL or set an env var and read it in `main.py`.

Testing after deploy

- Upload a real PDF from the frontend and run an analysis.
- Monitor Render logs and Vercel build logs if anything fails.

Optional: Docker alternative

- Create a `Dockerfile` in `backend/` and build/push to a container registry (Render also supports Docker). Use this if you need exact environment control.

Local quick commands

- Start backend locally from `backend/`:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

- Start frontend locally from `frontend/`:

```
npm install
npm run dev
```

If you want, I can now:

- Add an environment-variable-driven `VITE_API_URL` into `frontend/src/services/api.js` and example `.env` files
- Create a `Dockerfile` for the backend
- Commit and push these files and help you create Render and Vercel projects step-by-step

Which of those follow-ups would you like me to do now?
