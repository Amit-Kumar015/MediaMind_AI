from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio

from app.db import collection
from app.upload import vector_store_map
from app.ai import ask_ai
from app.rag import load_vector_store

router = APIRouter()

@router.post("/chat")
async def chat(file_id: str, question: str):
    # 🔍 fetch document
    doc = collection.find_one({"file_id": file_id})

    if not doc:
        return {"error": "File not found"}

    # 🔥 1. Try vector store (PDF case)
    db = load_vector_store(file_id)

    if db:
        docs = db.similarity_search(question, k=3)
        context = "\n".join([d.page_content for d in docs])
    else:
        # 🔥 fallback (audio or no vector)
        context = doc["content"][:8000]

    # 🤖 ask LLM
    answer = ask_ai(context, question)

    # 🔥 2. Timestamp logic (ONLY for audio)
    timestamp = None

    if doc.get("type") == "audio" and doc.get("segments"):
        best_match = None

        for seg in doc["segments"]:
            if any(word in seg["text"].lower() for word in answer.lower().split()):
                best_match = seg
                break

        if best_match:
            timestamp = best_match["start"]

    return {
        "answer": answer,
        "timestamp": timestamp
    }