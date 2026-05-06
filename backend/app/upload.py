from fastapi import APIRouter, UploadFile, File
from app.pdf import extract_text
from app.db import collection
import uuid
from app.rag import create_vector_store, save_vector_store
from app.audio import transcribe_audio

vector_store_map = {}

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{file_id}.pdf"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)

    db = create_vector_store(text)

    # 🔥 SAVE TO DISK
    save_vector_store(db, file_id)

    collection.insert_one({
        "file_id": file_id,
        "content": text
    })

    return {"file_id": file_id}
  
@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{file_id}.mp3"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text, segments = transcribe_audio(file_path)

    collection.insert_one({
        "file_id": file_id,
        "type": "audio",
        "content": text,
        "segments": segments
    })

    return {"file_id": file_id}