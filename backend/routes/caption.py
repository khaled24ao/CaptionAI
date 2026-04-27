from flask import Blueprint, Request, jsonify, request
from werkzeug.datastructures import FileStorage
from PIL import Image
import io
import base64
from flasgger import swag_from
from backend.services.ai_service import analyze_image
from backend.config.settings import get_settings
from backend.exceptions import (
    InvalidFileError, 
    FileSizeError, 
    UnsupportedFormatError,
    AIProcessingError
)
from backend.utils.logger import app_logger

caption_bp = Blueprint("caption", __name__)
settings = get_settings()

ALLOWED_EXTENSIONS: set[str] = set(settings.allowed_extensions)
MAX_FILE_SIZE: int = settings.max_file_size_mb * 1024 * 1024


def allowed_file(filename: str) -> bool:
    """Check if the filename has an allowed extension.
    
    Args:
        filename: Name of the file to check.
        
    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(file_data: bytes) -> bool:
    """Validate that the file data is a valid image.
    
    Args:
        file_data: Raw bytes of the image file.
        
    Returns:
        bool: True if the bytes represent a valid image, False otherwise.
    """
    try:
        img = Image.open(io.BytesIO(file_data))
        img.verify()
        return True
    except Exception:
        return False


@caption_bp.route("/api/v1/caption", methods=["POST"])
@swag_from({
    "tags": ["Caption"],
    "summary": "Generate AI caption for image",
    "description": "Upload an image to generate AI-powered caption, hashtags, alt text, and more",
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "name": "image",
            "in": "formData",
            "type": "file",
            "required": True,
            "description": "Image file (jpg, png, webp)"
        }
    ],
    "responses": {
        "200": {
            "description": "Successful response",
            "schema": {
                "type": "object",
                "properties": {
                    "result": {"type": "string"}
                }
            }
        },
        "400": {"description": "Bad request - no file or invalid file"},
        "413": {"description": "File too large"},
        "415": {"description": "Unsupported file format"},
        "500": {"description": "Internal server error"}
    }
})
def generate_caption() -> tuple[dict[str, str], int]:
    """Generate an AI caption for an uploaded image.
    
    Returns:
        tuple: JSON response dict and HTTP status code.
        
    Raises:
        InvalidFileError: If no file is provided or file is invalid.
        FileSizeError: If file exceeds maximum allowed size.
        UnsupportedFormatError: If file format is not allowed.
        AIProcessingError: If AI processing fails.
    """
    app_logger.info("Received caption request")
    
    if "image" not in request.files:
        app_logger.warning("No image file in request")
        raise InvalidFileError("No image file provided")
    
    file: FileStorage = request.files["image"]
    
    if file.filename == "":
        raise InvalidFileError("No file selected")
    
    if not allowed_file(file.filename):
        app_logger.warning(f"Invalid file format: {file.filename}")
        raise UnsupportedFormatError(
            f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    file_data: bytes = file.read()
    
    if len(file_data) > MAX_FILE_SIZE:
        raise FileSizeError(
            f"File too large. Maximum size is {settings.max_file_size_mb}MB"
        )
    
    if not validate_image(file_data):
        raise InvalidFileError("File is not a valid image")
    
    file.seek(0)
    img = Image.open(io.BytesIO(file_data))
    
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    
    buffer = io.BytesIO()
    img_format: str = img.format or "PNG"
    img.save(buffer, format=img_format)
    image_base64: str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    mime_type: str = f"image/{img_format.lower()}"
    
    try:
        result: str = analyze_image(image_base64, mime_type)
        app_logger.info("Caption generated successfully")
        return jsonify({"result": result}), 200
    except AIProcessingError:
        raise
    except Exception as e:
        app_logger.error("AI processing failed: %s", str(e))
        raise AIProcessingError(f"Failed to generate caption: {str(e)}") from e