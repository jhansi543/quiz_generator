import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .scraper import scrape_wikipedia
from .llm_quiz_generator import generate_quiz as generate_quiz_llm
from .database import get_database, close_database
from .models import GenerateRequest
from bson import ObjectId

load_dotenv()

_allowed = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
# Allow a special value '*' to mean all origins. When allowing all origins,
# browsers will reject responses that set Access-Control-Allow-Credentials to true,
# so we disable credentials in that case.
if _allowed.strip() == "*":
    ALLOWED_ORIGINS = ["*"]
    ALLOW_CREDENTIALS = False
else:
    ALLOWED_ORIGINS = [o.strip() for o in _allowed.split(",") if o.strip()]
    ALLOW_CREDENTIALS = True

app = FastAPI(title="AI Wiki Quiz Generator - Backend (project_tracer)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_event():
    await close_database()


@app.post("/generate_quiz")
async def generate_quiz(payload: GenerateRequest):
    url = payload.url
    try:
        title, summary, full_text = await scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to scrape URL: {e}")

    # Call the LLM generator (attempt Gemini via LangChain, fallback to placeholder)
    llm_result = await generate_quiz_llm(title, summary, full_text)

    # We intentionally do not store a separate 'summary' field anymore.
    doc = {
        "url": url,
        "title": title,
        # store the raw extracted article text so frontends can show the source material
        "full_text": full_text,
        "key_entities": llm_result.get("key_entities", {}),
        "sections": llm_result.get("sections", []),
        "quiz": llm_result.get("quiz", []),
        "related_topics": llm_result.get("related_topics", []),
    }

    db = get_database()
    res = await db.quizzes.insert_one(doc)

    # Read the stored document back and convert the ObjectId to string for JSON
    stored = await db.quizzes.find_one({"_id": res.inserted_id})
    if stored:
        stored["id"] = str(stored.pop("_id"))
        return stored

    # Fallback: return best-effort doc with id
    doc["id"] = str(res.inserted_id)
    return doc


@app.get("/history")
async def history():
    db = get_database()
    # exclude large fields from history listing (full_text may be large)
    cursor = db.quizzes.find({}, {"quiz": 0, "summary": 0, "key_entities": 0, "full_text": 0})
    items = []
    async for doc in cursor:
        items.append({
            "id": str(doc.get("_id")),
            "url": doc.get("url"),
            "title": doc.get("title"),
            "date_generated": str(doc.get("_id").generation_time) if doc.get("_id") else None
        })
    return items


@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    db = get_database()
    try:
        oid = ObjectId(quiz_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid quiz id")
    doc = await db.quizzes.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Quiz not found")
    doc["id"] = str(doc.pop("_id"))
    return doc
