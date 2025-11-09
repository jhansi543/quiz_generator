# Backend — project_tracer

This folder contains a minimal FastAPI backend scaffold for the AI Wiki Quiz Generator.

## Goals

- Scrape a Wikipedia URL
- Generate a quiz (placeholder LLM implementation)
- Store results in MongoDB
- Expose endpoints for generate and retrieving history

## Quick setup (Windows PowerShell, Python 3.10)

1. Create and activate a virtual environment (Python 3.10):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill values (MONGODB_URI, GEMINI_API_KEY if available):

```powershell
copy .env.example .env
```

4. Run the server (from `project_tracer` root):

```powershell
uvicorn backend.main:app --reload --port 8000
```

5. Test endpoints (recommended with an API tool or curl/Postman):

- POST `http://localhost:8000/generate_quiz` with JSON body `{ "url": "https://en.wikipedia.org/wiki/Alan_Turing" }`
- GET `http://localhost:8000/history`
- GET `http://localhost:8000/quiz/{id}`

## Notes

- Currently `llm_quiz_generator.py` contains a placeholder generator. To integrate Gemini/LLM, update that module and use LangChain (requires API key).
- `llm_quiz_generator.py` will now attempt to use LangChain + Gemini (langchain-google-genai). If not available, it falls back to the placeholder.
- MongoDB is required. You can run locally or use MongoDB Atlas. Set `MONGODB_URI` accordingly.
