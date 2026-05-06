from fastapi import FastAPI
from app.upload import router as upload_router
from app.chat import router as chat_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(chat_router)