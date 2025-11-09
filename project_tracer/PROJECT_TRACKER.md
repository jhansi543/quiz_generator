# Project Tracker — project_tracer

This file tracks progress, decisions, and next steps for the FastAPI + MongoDB + React + Tailwind + Gemini project.

## Goal

Implement a FastAPI backend that scrapes a Wikipedia URL, produces a quiz (via LLM), stores results in MongoDB, and exposes endpoints for generation and history. Then build a React + Tailwind frontend and deploy the frontend to Vercel.

## Status Summary

- Backend scaffold: in progress
- Frontend scaffold: not started
- LangChain/Gemini integration: placeholder created; needs API key integration and prompt engineering
- Deployment (Vercel): planned for frontend; backend can be deployed to a cloud host (Render, Fly, Railway) or Vercel Serverless Functions with adaptation

## Short-term checklist

- [x] Create project todo list (managed)
- [x] Create `project_tracer/backend/` scaffold with example files
- [ ] Create venv and install dependencies (instructions below)
- [ ] Configure `.env` with `MONGODB_URI` and `GEMINI_API_KEY`
- [ ] Run `uvicorn` and smoke-test endpoints

## Where we'll get required items

- Python 3.10: from https://www.python.org/downloads/
- MongoDB: local install (https://www.mongodb.com/try/download/community) or Atlas (https://www.mongodb.com/cloud/atlas)
- Gemini API key: Google Cloud / Vertex AI access (follow Google docs) — or substitute with another LLM provider and update `llm_quiz_generator.py`

## Notes & Decisions

- Backend will use `motor` (async MongoDB driver) and `httpx` + `beautifulsoup4` for scraping.
- Initial LLM implementation is a placeholder that returns sample quiz JSON; after we verify end-to-end we will wire LangChain + Gemini.

## Next actions (you can ask me to run these)

1. Create and activate venv, install requirements.
2. Populate `.env` with `MONGODB_URI` and (later) `GEMINI_API_KEY`.
3. Start the FastAPI backend: `uvicorn backend.main:app --reload --port 8000`.
4. Call POST `/generate_quiz` with `{ "url": "https://en.wikipedia.org/wiki/Alan_Turing" }` to test.

---

If you'd like, I can now:

- create the frontend scaffold (React + Tailwind), or
- integrate LangChain+Gemini in the backend placeholder (I will need your Gemini API key), or
- guide you step-by-step to create the venv and run the backend locally.
