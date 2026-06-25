from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone
from app.auth import get_current_user
from app.db import collection, chats_collection
from app.ai import ask_ai
from app.rag import load_vector_store

router = APIRouter()

class NewChatRequest(BaseModel):
    file_id: str

class ChatMessageRequest(BaseModel):
    chat_id: str
    question: str
    
@router.post("/chat/new")
async def create_new_chat(payload: NewChatRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    
    doc = collection.find_one({"file_id": payload.file_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="File not found or unauthorized")
        
    chat_id = str(uuid.uuid4())
    
    new_chat = {
        "chat_id": chat_id,
        "user_id": user_id,
        "file_id": payload.file_id,
        "title": f"Chat on {doc['filename']}",
        "messages": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    chats_collection.insert_one(new_chat)
    return {"chat_id": chat_id, "title": new_chat["title"]}

@router.get("/chats")
async def get_user_chats(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    chats = list(chats_collection.find({"user_id": user_id}, {"_id": 0}))
    return chats

@router.get("/chat/{chat_id}")
async def get_chat_history(chat_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    chat = chats_collection.find_one({"chat_id": chat_id, "user_id": user_id}, {"_id": 0})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return chat

@router.post("/chat")
async def chat(payload: ChatMessageRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]

    chat_session = chats_collection.find_one({"chat_id": payload.chat_id, "user_id": user_id})
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    file_id = chat_session["file_id"]
    doc = collection.find_one({"file_id": file_id, "user_id": user_id})

    db = load_vector_store(user_id, file_id)
    if db:
        docs = db.similarity_search(payload.question, k=3)
        context = "\n".join([d.page_content for d in docs])
    else:
        context = doc["content"][:8000]

    answer = ask_ai(context, payload.question)

    timestamp = None
    if doc.get("type") in ["audio", "video"] and doc.get("segments"):
        best_match = None
        for seg in doc["segments"]:
            if any(word in seg["text"].lower() for word in answer.lower().split()):
                best_match = seg
                break
        if best_match:
            timestamp = best_match["start"]

    user_msg = {"role": "user", "content": payload.question, "timestamp": None}
    ai_msg = {"role": "assistant", "content": answer, "timestamp": timestamp}

    chats_collection.update_one(
        {"chat_id": payload.chat_id},
        {"$push": {"messages": {"$each": [user_msg, ai_msg]}}}
    )

    return {
        "answer": answer,
        "timestamp": timestamp
    }