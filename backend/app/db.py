from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))
db = client["media_mind_db"]

collection = db["documents"]
users_collection = db["users"]
chats_collection = db["chats"]