from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    app_name: str = "CaptionAI"
    debug: bool = False
    groq_api_key: Optional[str] = Field(default=None, alias="GROQ_API_KEY")
    max_file_size_mb: int = 5
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp"]
    upload_folder: str = "storage/uploads"
    cors_origins: List[str] = ["*"]
    
    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return False
    
    def validate_api_key(self):
        if not self.groq_api_key or self.groq_api_key == "your_api_key_here":
            return False
        return True


def get_settings() -> Settings:
    return Settings()