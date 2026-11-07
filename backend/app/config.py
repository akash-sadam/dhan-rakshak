"""Configuration settings for Dhan-Rakshak.
Loads environment variables and sets defaults for Gnani.ai APIs.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    APP_NAME: str = "Dhan-Rakshak (ధన రక్షక్ / धन रक्षक)"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Gnani.ai API Configuration
    GNANI_API_KEY: str = Field(default_factory=lambda: os.getenv("GNANI_API_KEY", "gnani_demo_key_77a94f1c"))
    GNANI_BASE_URL: str = Field(default_factory=lambda: os.getenv("GNANI_BASE_URL", "https://api.vachana.ai"))
    
    # Prisma STT Config
    PRISMA_STT_URL: str = Field(default_factory=lambda: os.getenv("PRISMA_STT_URL", "https://api.vachana.ai/api/v1/stt/inference"))
    PRISMA_WS_URL: str = Field(default_factory=lambda: os.getenv("PRISMA_WS_URL", "wss://api.vachana.ai/api/v1/stt"))
    PRISMA_MODEL: str = "prisma-v3.0"

    # Evon 30B MoE LLM Config
    EVON_BASE_URL: str = Field(default_factory=lambda: os.getenv("EVON_BASE_URL", "https://api.vachana.ai/api/v1/chat/completions"))
    EVON_MODEL: str = "evon-30b-moe"

    # Timbre TTS Config
    TIMBRE_TTS_URL: str = Field(default_factory=lambda: os.getenv("TIMBRE_TTS_URL", "https://api.vachana.ai/api/v1/tts/inference"))
    TIMBRE_MODEL: str = "timbre-v3.0"

    # Emergency SOS Dispatch Config
    EMERGENCY_CONTACT_NAME: str = "Akash (Son)"
    EMERGENCY_CONTACT_PHONE: str = "+91 98480 22338"
    EMERGENCY_WEBHOOK_URL: Optional[str] = Field(default_factory=lambda: os.getenv("EMERGENCY_WEBHOOK_URL", None))

    # Simulation / Mock Fallback
    ENABLE_LIVE_GNANI_FALLBACK: bool = True


settings = Settings()
