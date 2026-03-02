# app/models/schemas.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
import numpy as np

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Convert NumPy types to Python native"""
        return cls(
            base=float(data.get('base', 0)),
            intensity_multiplier=float(data.get('intensity_multiplier', 1.0)),
            context_multiplier=float(data.get('context_multiplier', 1.0)),
            context_detected=str(data.get('context_detected', 'default')),
            final=float(data.get('final', 0))
        )


class RiskScore(BaseModel):
    """Risk score information"""
    score: float = Field(..., ge=0, le=100)
    breakdown: RiskBreakdown
    level: str = Field(..., pattern="^(low|medium|high|none)$")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            score=float(data.get('score', 0)),
            breakdown=RiskBreakdown.from_dict(data.get('breakdown', {})),
            level=str(data.get('level', 'low'))
        )

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            pattern_type=int(data.get('pattern_type', 0)),
            pattern_name=str(data.get('pattern_name', 'none')),
            risk_score=RiskScore.from_dict(data.get('risk_score', {})),
            explanation=str(data.get('explanation', '')),
            ethical_recommendation=data.get('ethical_recommendation', {}),
            confidence=float(data.get('confidence', 0.0)) if data.get('confidence') else None
        )

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str

    model_loaded: bool
