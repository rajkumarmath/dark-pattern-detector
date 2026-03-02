from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = os.getenv("APP_NAME", "Dark Pattern Detector API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Settings
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    CORS_ORIGINS: List[str] = ["*"]  # Parse from env if needed
    
    # Model Settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/models/ml_models/classifier.pkl")
    FEATURE_EXTRACTOR_PATH: str = os.getenv("FEATURE_EXTRACTOR_PATH", "app/models/ml_models/feature_extractor.pkl")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    class Config:
        env_file = ".env"

settings = Settings()
