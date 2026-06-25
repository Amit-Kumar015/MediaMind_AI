import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Lazy-load the app client to avoid hanging imports"""
    from backend.main import app
    return TestClient(app)

def test_chat_invalid_file(client):
    response = client.post(
        "/chat",
        params={
            "file_id": "invalid",
            "question": "test"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "error" in data
    
def test_chat_flow(client):
    with open("sample.pdf", "rb") as f:
        upload = client.post(
            "/upload",
            files={"file": ("sample.pdf", f, "application/pdf")}
        )

    data = upload.json()

    assert "file_id" in data

    file_id = data["file_id"]

    response = client.post(
        "/chat",
        params={
            "file_id": file_id,
            "question": "What is this document about?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data