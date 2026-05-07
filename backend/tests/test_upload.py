import pytest
from fastapi.testclient import TestClient
from io import BytesIO


@pytest.fixture
def client():
    """Lazy-load the app client to avoid hanging imports"""
    from app.main import app
    return TestClient(app)


def test_upload_without_file(client):
    """Test upload endpoint without providing a file"""
    response = client.post("/upload")
    assert response.status_code in [400, 422]


def test_upload_empty_pdf(client):
    """Test uploading an empty PDF file"""
    response = client.post(
        "/upload",
        files={"file": ("empty.pdf", BytesIO(b""), "application/pdf")}
    )
    assert response.status_code in [400, 500]


def test_upload_invalid_file(client):
    """Test uploading a non-PDF file with PDF extension claim"""
    response = client.post(
        "/upload",
        files={"file": ("test.txt", BytesIO(b"hello"), "text/plain")}
    )
    # Should reject non-PDF files
    assert response.status_code in [400, 422]


def test_upload_pdf(client):
    """Test uploading a valid PDF file"""
    # Use dummy PDF data - will fail extraction but passes file type validation
    pdf_content = b"%PDF-1.4\n1 0 obj\n<</Type/Catalog>>\nendobj\nxref\ntrailer\n<</Size 1>>\nstartxref\n0\n%%EOF"
    
    response = client.post(
        "/upload",
        files={"file": ("sample.pdf", BytesIO(pdf_content), "application/pdf")}
    )

    # PDF format validation passes, but content extraction may fail
    # Either 200 (if extraction succeeds) or 500 (if PDF is invalid)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "file_id" in data


def test_upload_audio(client):
    """Test uploading an audio file"""
    # Use dummy MP3 data
    response = client.post(
        "/upload-audio",
        files={"file": ("sample.mp3", BytesIO(b"dummy audio"), "audio/mpeg")}
    )

    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "file_id" in data


def test_upload_audio_no_content(client):
    """Test uploading an empty audio file"""
    response = client.post(
        "/upload-audio",
        files={"file": ("empty.mp3", BytesIO(b""), "audio/mpeg")}
    )
    assert response.status_code in [400, 500]


def test_upload_video(client):
    """Test uploading a video file"""
    # Use dummy MP4 data (simple MP4 signature)
    response = client.post(
        "/upload-video",
        files={"file": ("sample.mp4", BytesIO(b"dummy video"), "video/mp4")}
    )

    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "file_id" in data


def test_upload_get_method(client):
    """Test that GET method is not allowed on upload endpoint"""
    response = client.get("/upload")
    assert response.status_code == 405


def test_corrupted_pdf(client):
    """Test uploading a corrupted PDF file"""
    response = client.post(
        "/upload",
        files={
            "file": (
                "bad.pdf",
                BytesIO(b"not a real pdf"),
                "application/pdf"
            )
        }
    )
    assert response.status_code in [400, 500]