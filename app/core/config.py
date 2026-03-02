# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = "Dark Pattern Detector API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Settings
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["*"]
    
    # Model Settings
    MODEL_PATH: str = "app/models/ml_models/classifier.pkl"
    FEATURE_EXTRACTOR_PATH: str = "app/models/ml_models/feature_extractor.pkl"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()