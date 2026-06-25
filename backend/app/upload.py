from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from app.auth import get_current_user, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.pdf import extract_text
from app.db import collection
import uuid
from app.rag import create_vector_store, save_vector_store
from app.audio import transcribe_audio
import os
import traceback
import jwt

vector_store_map = {}

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="File is empty")
            f.write(content)

        # Extract text
        text = extract_text(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
          
        user_id = current_user["user_id"]

        # Create vector store
        db = create_vector_store(text)

        # Save to disk
        save_vector_store(db, user_id, file_id)

        # Store in database
        collection.insert_one({
        "file_id": file_id,
        "user_id": user_id,
        "filename": file.filename,
        "content": text,
        "type": "pdf"
        })

        return {"file_id": file_id}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
  
@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["user_id"]

        # Validate file type
        if not any(file.filename.lower().endswith(ext) for ext in ['.mp3', '.wav', '.m4a', '.ogg']):
            raise HTTPException(status_code=400, detail="Only audio files are allowed (mp3, wav, m4a, ogg)")
        
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp3")

        # Save file
        with open(file_path, "wb") as f:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="File is empty")
            f.write(content)

        # Transcribe audio
        text, segments = transcribe_audio(file_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
  
        # Store in database
        collection.insert_one({
            "file_id": file_id,
            "user_id": user_id,
            "filename": file.filename,
            "type": "audio",
            "content": text,
            "segments": segments
        })

        return {"file_id": file_id}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading audio: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
      
@router.post("/upload-video")
async def upload_video(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
  try:
    file_id = str(uuid.uuid4())
    user_id = current_user["user_id"]

    # preserve extension
    extension = file.filename.split(".")[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{extension}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 🔥 Whisper works directly on video
    text, segments = transcribe_audio(file_path)

    collection.insert_one({
        "file_id": file_id,
        "user_id": user_id,
        "filename": file.filename,
        "type": "video",
        "content": text,
        "segments": segments
    })

    return {"file_id": file_id}
  
  except HTTPException:
        raise
  except Exception as e:
      print(f"Error uploading video: {str(e)}")
      print(traceback.format_exc())
      raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/media/{file_id}")
async def get_media(file_id: str, request: Request, token: str = Query(None)):
    active_token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        active_token = auth_header.split(" ")[1]
        
    elif token:
        active_token = token

    if not active_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(active_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token session payload")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token signature expired or invalid")

    doc = collection.find_one({"file_id": file_id, "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Media asset not found or unauthorized")

    file_type = doc.get("type")
    if file_type == "audio":
        path = os.path.join(UPLOAD_DIR, f"{file_id}.mp3")
    elif file_type == "video":
        path = None
        for f in os.listdir(UPLOAD_DIR):
            if f.startswith(file_id) and not f.endswith(".pdf") and not f.endswith(".mp3"):
                path = os.path.join(UPLOAD_DIR, f)
                break
    else:
        raise HTTPException(status_code=400, detail="Not a playable media resource")

    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Physical stream file missing on host")

    return FileResponse(path)