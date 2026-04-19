from groq import Groq
import os
from typing import Optional
from backend.config.settings import get_settings
from backend.utils.logger import ai_logger

_client: Optional[Groq] = None


def get_client() -> Groq:
    global _client
    if _client is None:
        settings = get_settings()
        if not settings.validate_api_key():
            raise ValueError("GROQ_API_KEY is not set. Please configure your .env file.")
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def analyze_image(image_base64: str, mime_type: str) -> str:
    client = get_client()
    ai_logger.info(f"Analyzing image with mime_type: {mime_type}")
    
    response = client.chat.completions.create(
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
    ai_logger.info("Image analysis completed successfully")
    return result