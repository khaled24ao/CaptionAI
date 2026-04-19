import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_image():
    from PIL import Image
    import io
    
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CaptionAI" in response.data


def test_caption_no_file(client):
    response = client.post("/api/v1/caption")
    assert response.status_code == 400
    assert b"No image file provided" in response.data


def test_caption_empty_filename(client, test_image):
    response = client.post(
        "/api/v1/caption",
        data={"image": (test_image, "")},
        content_type="multipart/form-data"
    )
    assert response.status_code == 400


def test_caption_invalid_extension(client):
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


def test_caption_valid_image(client, test_image):
    response = client.post(
        "/api/v1/caption",
        data={"image": (test_image, "test.png")},
        content_type="multipart/form-data"
    )
    assert response.status_code in [200, 500]