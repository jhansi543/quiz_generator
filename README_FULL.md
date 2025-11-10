# Project Tracer — Quiz Generator (End-to-end)

This repository contains a full-stack project that scrapes a Wikipedia article, generates quiz questions (via LLMs or a deterministic fallback), stores results in MongoDB, and exposes a chat-like frontend to view history and generated quizzes.

This README documents the system end-to-end, how to run it locally, how to deploy, what environment variables are required, and where to add UI screenshots for your project documentation.

---

## Table of contents

- Project overview
- Architecture
- Tech stack
- Local development (backend + frontend)
- Environment variables (backend + frontend)
- API endpoints
- Deployment notes (Vercel gotchas, recommended Render flow)
- Troubleshooting
- Screenshots (where and how to add)

---

## Project overview

- Backend: FastAPI app that scrapes a URL, generates quiz questions, stores quiz documents in MongoDB, and exposes endpoints to create quizzes and list history.
- Frontend: React + Vite + Tailwind UI — chat-style interface. The frontend reads the backend base URL from `VITE_API_BASE` at build time.
- Persistence: MongoDB (motor / AsyncIOMotorClient)
- Containerization: a `Dockerfile` is provided for container hosts (Render, Railway, Fly, HF Spaces).

---

## Architecture

1. User pastes a Wikipedia URL into the frontend.
2. Frontend calls `POST /generate_quiz` on the backend.
3. Backend scrapes the article, calls LLM orchestration (Gemini / OpenAI / HF router / local fallback), produces a JSON quiz, and stores it in MongoDB.
4. Frontend can fetch `GET /history` and `GET /quiz/{id}` to display stored quizzes and source text.

---

## Tech stack

- Backend: Python 3.10, FastAPI, Uvicorn, Motor, httpx, BeautifulSoup
- Frontend: React (18) + Vite, TailwindCSS, Axios
- Database: MongoDB (Atlas recommended for production)
- Deployment: Docker-friendly (Render/Railway/Fly/HF) or Vercel with advanced config

---

## Local development

Prerequisites

- Python 3.10
- Node 18+ (npm)
- MongoDB (local) or MongoDB Atlas connection string

Backend (recommended commands for PowerShell)

```powershell
cd project_tracer/backend
python -m venv .venv
# activate venv in PowerShell
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# create a .env file (see env vars below)
uvicorn main:app --host 127.0.0.1 --port 8003 --reload
```

Frontend

```powershell
cd project_tracer/frontend
npm install
# optionally set VITE_API_BASE in local .env (Vite will read .env files)
# VITE_API_BASE=http://127.0.0.1:8003
npm run dev
```

Notes
- The frontend reads `import.meta.env.VITE_API_BASE` during build. If not provided it falls back to `http://127.0.0.1:8003`.
- The backend `database.py` tries to load a `.env` file in the `backend/` folder first.

---

## Environment variables

Backend (required)

- `MONGODB_URI` — MongoDB connection string (example: `mongodb://user:pass@host:27017` or Atlas `mongodb+srv://...`)
- `DATABASE_NAME` — database name (default `project_tracer_db`)
- `ALLOWED_ORIGINS` — comma-separated list of allowed origins for CORS (e.g., `http://localhost:5173,https://your-frontend.vercel.app`) or `*` for development testing

Backend (optional for LLMs)

- `OPENAI_API_KEY` — OpenAI API key for OpenAI fallback
- `HF_API_TOKEN` — Hugging Face token
- `USE_LOCAL_MODEL` — `true`/`false` to enable local transformer fallback
- `GEN_MODEL`, `SUM_MODEL` — optional model names used by orchestration

Frontend (Vite build)

- `VITE_API_BASE` — full backend base URL used at build-time (example: `https://your-backend.example.com`). Add this to your Vercel or hosting provider when you deploy the frontend.

How to add environment variables on Vercel (quick)

```powershell
# add to frontend project
cd project_tracer/frontend
vercel env add VITE_API_BASE production
# add to backend project
cd ../backend
vercel env add MONGODB_URI production
vercel env add ALLOWED_ORIGINS production
```

---

## API endpoints (backend)

- POST /generate_quiz
  - payload: { "url": "https://en.wikipedia.org/xyz" }
  - response: stored quiz document (includes `id`, `title`, `full_text`, `quiz`, etc.)

- GET /history
  - response: list of recent stored quizzes (lightweight: no full_text)

- GET /quiz/{id}
  - response: full stored document including `full_text` and `quiz`

- GET /health
  - response: { "status": "ok" } (simple readiness check)

---

## Deployment notes & recommendations

Vercel notes

- Vercel can run Python serverless functions, but your app is designed as a long-running Uvicorn process (Docker). Vercel's Docker builder (`@vercel/docker`) may not be available in some CLI / account setups and can fail. When Vercel auto-detects the project as Python serverless it will not run your Dockerfile and API routes may return 404.
- If you want to keep Vercel, either deploy a registry image or refactor to serverless functions. That is more complex.

Recommended: use a container host (Render, Railway, Fly, Hugging Face Spaces)

- These providers accept a `Dockerfile` directly and will run Uvicorn as a long-lived process which matches this project architecture.
- Render example: create a new Web Service -> Connect repo -> choose `project_tracer/backend` -> Deploy using Dockerfile. Set environment variables in the Render dashboard.

Deploy frontend to Vercel (simple)

- The frontend is a static/Vite app and works well on Vercel. Make sure to add `VITE_API_BASE` to the frontend project settings before deploying so the built bundle calls the correct backend URL.

---

## Troubleshooting

Problem: `/history` returns 500 in production
- Cause: backend cannot connect to MongoDB (missing `MONGODB_URI` or network/Atlas IP access blocked)
- Fix: set `MONGODB_URI` in production envs and ensure Atlas IP access list allows your hosting provider (for quick tests add `0.0.0.0/0`).

Problem: CORS preflight OPTIONS returns 400
- Cause: `ALLOWED_ORIGINS` is not configured for your frontend domain.
- Fix: set `ALLOWED_ORIGINS` to the frontend origin or `*` while testing.

Problem: Vercel returns 404 for API routes
- Cause: Vercel ran project as static or serverless and didn't run your Docker process.
- Fix: use a container host or deploy a registry image and configure Vercel accordingly.

---

## Screenshots

Add UI screenshots here to document the app visually. Create `project_tracer/frontend/assets/screenshots/` and place image files with these suggested names:

- `frontend-chat.png` — main chat UI showing generated quiz
- `frontend-history.png` — History panel with multiple items
- `backend-health.png` — curl output or health check response
- `deployment-logs.png` — useful logs from your hosting provider

Then include them in this README by replacing the placeholder markdown below with real images (the placeholders already point to the expected paths):

### UI: Frontend — Chat

![Frontend Chat](frontend/assets/screenshots/frontend-chat.png)

### UI: Frontend — History

![Frontend History](frontend/assets/screenshots/frontend-history.png)

### Backend Health

![Backend Health](project_tracer/backend/assets/screenshots/backend-health.png)

### Deployment logs / Example

![Deployment Logs](project_tracer/backend/assets/screenshots/deployment-logs.png)

> Note: If images are not present, GitHub will render broken image placeholders. Commit your screenshots to the repo under the paths above to include them in the README.

---

## Notes and next steps

- Consider pinning versions in `requirements.txt` before production deploy.
- Add a `.dockerignore` to exclude `.venv`, `.env`, `.git`, `node_modules`, and build artifacts.
- If you want, I can prepare a `render.yaml` and instructions to deploy the backend to Render with one click.

---

If you'd like, I can now:
- generate a `render.yaml` for Render and add it to `project_tracer/backend/`, or
- run Vercel CLI to deploy the frontend (you'll be asked to paste `VITE_API_BASE`), or
- add `.dockerignore` and pin dependency versions.

Which would you like me to do next?
