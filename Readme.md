# AI-Powered Document & Multimedia Q&A Web Application

## Overview

This project is an AI-powered web application that allows users to upload PDFs, audio files, and video files and interact with them using a chatbot interface.

The system uses Retrieval-Augmented Generation (RAG) for intelligent document question answering and Whisper-based transcription for multimedia processing.

Users can:

* Upload PDF documents
* Upload audio/video files
* Ask questions related to uploaded content
* Get AI-generated answers
* Extract timestamps from audio/video
* Jump directly to relevant media segments

---

# Features

## Document Processing

* PDF upload support
* Automatic text extraction
* Semantic chunking using LangChain
* Vector search using FAISS

## AI Question Answering

* RAG-based contextual question answering
* Groq LLM integration
* Semantic retrieval using HuggingFace embeddings

## Audio & Video Processing

* Audio transcription using Whisper
* Video transcription using Whisper
* Timestamp extraction
* Media playback with timestamp navigation

## Frontend

* React + Vite frontend
* Modern Tailwind CSS UI
* Chat interface
* File upload interface
* Audio/video player integration

## Backend

* FastAPI backend
* MongoDB integration
* REST APIs
* Persistent FAISS vector storage

## DevOps & Testing

* Dockerized application
* Docker Compose setup
* GitHub Actions CI/CD

---

# Tech Stack

## Frontend

* React.js
* Vite
* Tailwind CSS
* Axios

## Backend

* FastAPI
* Python
* MongoDB
* LangChain
* FAISS
* Sentence Transformers
* Whisper
* Groq API

## DevOps

* Docker
* Docker Compose
* GitHub Actions

---

# Architecture

```text
Frontend (React)
        ↓
FastAPI Backend
        ↓
Document/Media Processing Layer
   ├── PDF Extraction
   ├── Whisper Transcription
   ├── Text Chunking
   └── Embedding Generation
        ↓
FAISS Vector Database
        ↓
Groq LLM
        ↓
AI Response + Timestamps
```

---

# Folder Structure

```text
project-root/
│
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
│
└── .github/
    └── workflows/
```

---

# Installation & Setup

## Clone Repository

```bash
git clone <repository-url>
cd project-root
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside backend:

```env
GROQ_API_KEY=your_groq_api_key
MONGO_URL=mongodb://localhost:27017
```

---

# Run Backend

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

## Install Dependencies

```bash
npm install
```

## Start Frontend

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# Docker Setup

## Run Complete Application

```bash
docker compose up --build
```

---


# Future Improvements

* User authentication
* Streaming AI responses
* Redis caching
* Cloud deployment
* Multi-user support
* Improved timestamp matching
* Real-time processing

---

# Author

Amit Kumar

---

# License

This project is developed for educational and assignment purposes.
