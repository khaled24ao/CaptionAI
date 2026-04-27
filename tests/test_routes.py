import pytest
from app import main


@pytest.fixture
def client():
    """Create a test client for the Flask app.
    
    Returns:
        Flask test client instance.
    """
    from app import main as create_app_func
    # Import and call main to get the app, but we need to modify it
    from dotenv import load_dotenv
    load_dotenv()
    from backend.app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_image():
    """Create a test image in memory.
    
    Returns:
        BytesIO buffer containing a test PNG image.
    """
    from PIL import Image
    import io
    
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def test_index_route(client) -> None:
    """Test the main index page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"CaptionAI" in response.data


def test_caption_no_file(client) -> None:
    """Test that caption endpoint returns 400 when no file is provided."""
    response = client.post("/api/v1/caption")
    assert response.status_code == 400
    assert b"No image file provided" in response.data


def test_caption_empty_filename(client, test_image) -> None:
    """Test that caption endpoint returns 400 for empty filename."""
    response = client.post(
        "/api/v1/caption",
        data={"image": (test_image, "")},
        content_type="multipart/form-data"
    )
    assert response.status_code == 400


def test_caption_invalid_extension(client) -> None:
    """Test that caption endpoint rejects invalid file extensions."""
    from PIL import Image
    import io
    
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="BMP")
    buffer.seek(0)
    
    response = client.post(
        "/api/v1/caption",
        data={"image": (buffer, "test.bmp")},
        content_type="multipart/form-data"
    )
    assert response.status_code == 415


def test_caption_valid_image(client, test_image) -> None:
    """Test that caption endpoint accepts valid images."""
    response = client.post(
        "/api/v1/caption",
        data={"image": (test_image, "test.png")},
        content_type="multipart/form-data"
    )
    # Expect either 200 (if API key valid) or 502 (AI processing error due to invalid key)
    assert response.status_code in [200, 502]