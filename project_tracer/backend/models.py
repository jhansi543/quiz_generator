from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    url: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: Optional[str] = "medium"
    explanation: Optional[str] = ""


class QuizOutput(BaseModel):
    id: Optional[str]
    url: str
    title: str
    summary: Optional[str]
    key_entities: Optional[dict] = {}
    sections: Optional[List[str]] = []
    quiz: List[QuizQuestion]
    related_topics: Optional[List[str]] = []
    date_generated: Optional[datetime] = Field(default_factory=datetime.utcnow)
