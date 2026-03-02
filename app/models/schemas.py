# app/models/schemas.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any

class DetectionRequest(BaseModel):
    """Request model for dark pattern detection"""
    text: Optional[str] = Field(None, description="Text content to analyze", max_length=5000)
    url: Optional[HttpUrl] = Field(None, description="URL to fetch and analyze")

class RiskBreakdown(BaseModel):
    """Detailed risk score breakdown"""
    base: float
    intensity_multiplier: float
    context_multiplier: float
    context_detected: str
    final: float

class RiskScore(BaseModel):
    """Risk score information"""
    score: float = Field(..., ge=0, le=100)
    breakdown: RiskBreakdown
    level: str = Field(..., pattern="^(low|medium|high|none)$")

class EthicalSuggestion(BaseModel):
    """Ethical design suggestions"""
    title: str
    alternatives: List[str]
    example: str

class DetectionResponse(BaseModel):
    """Response model for detection API"""
    pattern_type: int = Field(..., ge=0, le=5)
    pattern_name: str
    risk_score: RiskScore
    explanation: str
    ethical_recommendation: EthicalSuggestion
    confidence: Optional[float] = Field(None, ge=0, le=1)

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    model_loaded: bool