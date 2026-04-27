from groq import Groq
from groq.types.chat.chat_completion import ChatCompletion
import os
from typing import Optional
from backend.config.settings import get_settings
from backend.utils.logger import ai_logger
from backend.exceptions import AIProcessingError

_client: Optional[Groq] = None


def get_client() -> Groq:
    """Get or create the Groq API client.
    
    Returns:
        Groq: The Groq API client instance.
        
    Raises:
        AIProcessingError: If API key is not configured.
        ValueError: If GROQ_API_KEY is not set.
    """
    global _client
    if _client is None:
        settings = get_settings()
        if not settings.validate_api_key():
            raise AIProcessingError("GROQ_API_KEY is not set. Please configure your .env file.")
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def analyze_image(image_base64: str, mime_type: str) -> str:
    """Analyze an image using the Groq AI API to generate captions.
    
    Args:
        image_base64: Base64 encoded image data.
        mime_type: MIME type of the image (e.g., 'image/png').
        
    Returns:
        str: The AI-generated caption and metadata as JSON string.
        
    Raises:
        AIProcessingError: If image analysis fails or response is malformed.
        ValueError: If inputs are invalid.
    """
    if not image_base64 or not isinstance(image_base64, str):
        raise ValueError("image_base64 must be a non-empty string")
    if not mime_type or not isinstance(mime_type, str):
        raise ValueError("mime_type must be a non-empty string")
    
    try:
        client = get_client()
        ai_logger.info("Analyzing image with mime_type: %s", mime_type)
        
        response: ChatCompletion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image and return JSON only:\n{\n  caption: one professional sentence description,\n  detailed_description: 3 sentence detailed description,\n  hashtags: [10 relevant hashtags without #],\n  alt_text: accessibility alt text,\n  mood: the mood/feeling of the image,\n  use_cases: [3 suggested use cases]\n}"},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}}
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        result = response.choices[0].message.content
        if not result:
            raise AIProcessingError("AI returned empty response")
        
        ai_logger.info("Image analysis completed successfully")
        return result
    except ValueError as ve:
        ai_logger.error("Value error during image analysis: %s", str(ve))
        raise
    except AIProcessingError:
        raise
    except Exception as e:
        ai_logger.error("AI processing failed with unexpected error: %s", str(e))
        raise AIProcessingError(f"Failed to analyze image: {str(e)}") from e