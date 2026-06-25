import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

class HFEmbedding(Embeddings):
    def embed_documents(self, texts):
        return model.encode(texts).tolist()

    def embed_query(self, text):
        return model.encode([text])[0].tolist()


def create_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)
    embeddings = HFEmbedding()
    db = FAISS.from_texts(chunks, embeddings)
    return db
  
def save_vector_store(db, user_id, file_id):
    path = f"vectorstores/{user_id}/{file_id}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    db.save_local(path)
    
def load_vector_store(user_id, file_id):
    path = f"vectorstores/{user_id}/{file_id}"
    if os.path.exists(path):
        embeddings = HFEmbedding()
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    return None