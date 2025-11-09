from typing import List, Dict, Optional
import os
import json
import logging
from .models import QuizQuestion
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def generate_quiz_placeholder(title: str, summary: str, full_text: str) -> Dict:
    """Placeholder quiz generator.

    Returns a small deterministic quiz structure. Used as fallback when LLM is not available.
    """
    q1 = QuizQuestion(
        question=f"What is the main subject of the article '{title}'?",
        options=[title, "Something else", "Another topic", "None of the above"],
        answer=title,
        difficulty="easy",
        explanation="The article title names the main subject."
    )

    q2 = QuizQuestion(
        question="Which of the following is mentioned in the summary?",
        options=["A mentioned fact", "Not mentioned", "Unknown", "Irrelevant"],
        answer="A mentioned fact",
        difficulty="medium",
        explanation="Placeholder: the real LLM will ground this in the article text."
    )
    # Build a larger set of placeholder questions (7-8 items) to match caller expectations
    q3 = QuizQuestion(
        question="Which year is most closely associated with the topic?",
        options=["Early 1900s", "Mid 20th century", "Late 20th century", "21st century"],
        answer="Mid 20th century",
        difficulty="medium",
        explanation="Placeholder: temporal context referenced in the article."
    )

    q4 = QuizQuestion(
        question="Which of these would be considered a key term related to the article?",
        options=["Key term A", "Key term B", "Key term C", "Key term D"],
        answer="Key term A",
        difficulty="easy",
        explanation="Placeholder key term used for demonstration."
    )

    q5 = QuizQuestion(
        question="Which region is primarily discussed in the article?",
        options=["Global", "Region A", "Region B", "Local"],
        answer="Global",
        difficulty="medium",
        explanation="Placeholder: the article often addresses a broad/global context."
    )

    q6 = QuizQuestion(
        question="What is a common application or use-case mentioned?",
        options=["Application A", "Application B", "Application C", "Application D"],
        answer="Application A",
        difficulty="medium",
        explanation="Placeholder application used as an example."
    )

    q7 = QuizQuestion(
        question="Which of the following is an important subtopic?",
        options=["Subtopic 1", "Subtopic 2", "Subtopic 3", "Subtopic 4"],
        answer="Subtopic 1",
        difficulty="hard",
        explanation="Placeholder subtopic for depth."
    )

    q8 = QuizQuestion(
        question="Which statement best summarizes a likely conclusion from the article?",
        options=["Conclusion A", "Conclusion B", "Conclusion C", "Conclusion D"],
        answer="Conclusion A",
        difficulty="hard",
        explanation="Placeholder summary/conclusion."
    )

    related = ["Related topic 1", "Related topic 2"]

    return {
        "quiz": [q1.dict(), q2.dict(), q3.dict(), q4.dict(), q5.dict(), q6.dict(), q7.dict(), q8.dict()],
        "related_topics": related,
        "key_entities": {"people": [], "organizations": [], "locations": []},
        "sections": []
    }


async def generate_quiz_with_gemini(title: str, summary: str, full_text: str) -> Dict:
    """Attempt to generate a quiz using LangChain + Google Gemini (via langchain-google-genai).

    This function will try to import a LangChain Google LLM wrapper. If unavailable or the
    call fails, it raises an exception so the caller can fallback to the placeholder.
    """
    # Lazy import to avoid hard dependency failure
    try:
        # Try a couple of plausible imports for different langchain versions
        try:
            from langchain import GoogleGenAI  # newer wrapper
            LLMClass = GoogleGenAI
        except Exception:
            try:
                from langchain.llms import GoogleGenAI as LLMClass
            except Exception:
                # If import fails, raise for fallback
                raise ImportError("langchain Google GenAI LLM not available. Install langchain-google-genai.")

        # Build a structured prompt instructing the model to output strict JSON
        system_prompt = (
            "You are an assistant that extracts quiz questions from a Wikipedia article. "
            "Given the article title and the article text, produce a JSON object with the following keys:\n"
            "- url (optional)\n- title\n- summary (optional)\n- key_entities (object with people/organizations/locations lists)\n- sections (list of section titles)\n- related_topics (list of strings)\n- quiz (list of questions)\n"
            "Produce between 7 and 8 quiz questions (aim for 8). Each question must be an object with: question (string), options (array of 3-5 strings), answer (one of the options), difficulty (easy|medium|hard), explanation (string)."
            "Respond with only valid JSON that matches the described shape. Do not include any extra commentary."
        )

        # We no longer include a separate summary; pass title and article text only.
        user_prompt = (
            f"TITLE:\n{title}\n\nARTICLE:\n{full_text[:15000]}\n\n"
            "Return JSON only."
        )

        # Initialize LLM — relies on GOOGLE_APPLICATION_CREDENTIALS env var set to the JSON path
        llm = LLMClass()

        # Call the LLM (different langchain versions vary; many support __call__)
        resp_text = None
        try:
            resp_text = llm(system_prompt + "\n\n" + user_prompt)
        except TypeError:
            # Some wrappers require a different interface
            try:
                resp = llm.generate([system_prompt + "\n\n" + user_prompt])
                # extract text from response structure
                resp_text = resp.generations[0][0].text
            except Exception as e:
                raise RuntimeError(f"LLM call failed: {e}")

        if not resp_text:
            raise RuntimeError("Empty response from LLM")

        # Parse JSON defensively
        try:
            parsed = json.loads(resp_text)
        except Exception as e:
            raise ValueError(f"Failed to parse JSON from LLM response: {e}\nResponse text: {resp_text[:1000]}")

        # Basic validation - ensure 'quiz' is present and questions have required fields
        if "quiz" not in parsed:
            raise ValueError("LLM JSON did not include 'quiz' key")

        # Validate each question using Pydantic model
        validated_questions = []
        for q in parsed.get("quiz", []):
            try:
                qq = QuizQuestion(**q)
                validated_questions.append(qq.dict())
            except ValidationError as ve:
                logger.warning("Question validation failed: %s", ve)

        parsed["quiz"] = validated_questions
        # Ensure keys exist
        parsed.setdefault("related_topics", [])
        parsed.setdefault("key_entities", {"people": [], "organizations": [], "locations": []})
        parsed.setdefault("sections", [])

        return parsed

    except Exception as e:
        # Propagate exception so caller can fallback and log
        logger.exception("Gemini/LangChain generation failed: %s", e)
        raise


async def generate_quiz(title: str, summary: str, full_text: str) -> Dict:
    """Public entrypoint: try Gemini via LangChain, otherwise fallback to placeholder.
    """
    # Try Gemini integration first
    try:
        result = await generate_quiz_with_gemini(title, summary, full_text)
        return result
    except Exception:
        logger.info("Falling back to placeholder generator.")
        return await generate_quiz_placeholder(title, summary, full_text)
