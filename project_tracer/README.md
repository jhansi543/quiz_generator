# project_tracer — AI Wiki Quiz Generator (scaffold)

This repository contains a scaffold for the DeepKlarity assignment: FastAPI backend + MongoDB, a React + Tailwind frontend (not created yet), and integration points for LangChain + Gemini.

What's included:

- `project_tracer/backend/` — FastAPI backend scaffold (scraper, placeholder LLM, MongoDB integration)

What I need from you to continue:

- A MongoDB connection string (local or Atlas) to run end-to-end.
- (Optional) Gemini API key (or another LLM provider) to wire LangChain in `llm_quiz_generator.py`.

Next steps I can take when you say go:

- Integrate LangChain + Gemini (you must provide the API key or confirm using a different model).
- Build the React + Tailwind frontend and wire it to the backend.
- Add caching and raw HTML storage and implement the 'Take Quiz' mode.

To get the backend running locally (Windows PowerShell):

```powershell
# create venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r backend\requirements.txt

# copy env example and edit
copy backend\.env.example backend\.env
# edit backend\.env and set MONGODB_URI

# run server
uvicorn backend.main:app --reload --port 8000
```

If you'd like, I'll now integrate LangChain + Gemini, but I will need your GEMINI_API_KEY (or permission to use another LLM).
