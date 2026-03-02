# app/api/endpoints.py
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from typing import Optional, List
from pydantic import BaseModel
import tempfile
import os

from app.models.schemas import DetectionRequest, DetectionResponse, HealthCheck
from app.services.multimodal_detector import MultiModalDetector

router = APIRouter()

# Request/Response models for new endpoints
class BatchRequest(BaseModel):
    texts: List[str]

class SolutionRequest(BaseModel):
    pattern_type: int
    context: Optional[str] = "default"

# Dependency
def get_detector():
    return MultiModalDetector()

@router.get("/health", response_model=HealthCheck)
async def health_check(detector: MultiModalDetector = Depends(get_detector)):
    """
    Health check endpoint
    """
    return HealthCheck(
        status="healthy",
        version="2.0.0",  # Upgraded to multi-modal
        model_loaded=detector.text_detector.models_loaded
    )

@router.post("/detect")
async def detect_dark_patterns(
    request: DetectionRequest,
    detector: MultiModalDetector = Depends(get_detector)
):
    """
    Detect dark patterns in text or URL
    """
    try:
        if request.url:
            result = detector.detect_from_url(str(request.url))
        else:
            result = detector.detect_from_text(request.text or "")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"🔥 API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.post("/detect/screenshot")
async def detect_from_screenshot(
    file: UploadFile = File(...),
    detector: MultiModalDetector = Depends(get_detector)
):
    """
    Detect dark patterns from screenshot upload
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Analyze screenshot
        result = detector.detect_from_screenshot(tmp_path)
        
        # Clean up
        os.unlink(tmp_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Screenshot analysis failed: {str(e)}")

@router.post("/solutions")
async def get_solutions(
    request: SolutionRequest,
    detector: MultiModalDetector = Depends(get_detector)
):
    """
    Get ethical solutions for a detected pattern
    """
    try:
        # Create a dummy detection result with the pattern type
        detection = {"pattern_type": request.pattern_type}
        solutions = detector.get_solutions(detection)
        return solutions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-with-solutions")
async def analyze_and_solve(
    request: DetectionRequest,
    detector: MultiModalDetector = Depends(get_detector)
):
    """
    Complete analysis: detect patterns AND provide solutions
    """
    try:
        # Detect patterns
        if request.url:
            detection = detector.detect_from_url(str(request.url))
        else:
            detection = detector.detect_from_text(request.text or "")
        
        # Get solutions
        solutions = detector.get_solutions(detection)
        
        # Generate improvement report
        report = detector.generate_improvement_report(detection)
        
        return {
            "detection": detection,
            "solutions": solutions,
            "improvement_report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect/batch")
async def detect_batch(
    request: BatchRequest,
    detector: MultiModalDetector = Depends(get_detector)
):
    """
    Analyze multiple texts in one request
    """
    results = []
    for text in request.texts:
        try:
            result = detector.detect_from_text(text)
            results.append({
                "text": text[:100] + "...",
                "result": result
            })
        except Exception as e:
            results.append({
                "text": text[:100] + "...",
                "error": str(e)
            })
    
    return {"results": results, "total": len(results)}

@router.get("/patterns")
async def list_patterns():
    """
    List all supported dark pattern types
    """
    return {
        "patterns": [
            {"id": 0, "name": "none", "description": "No dark pattern detected"},
            {"id": 1, "name": "forced_action", "description": "Forces user to take action"},
            {"id": 2, "name": "confirmshaming", "description": "Guilts user into choice"},
            {"id": 3, "name": "hidden_costs", "description": "Hidden fees revealed late"},
            {"id": 4, "name": "interface_interference", "description": "Hides preferred options"},
            {"id": 5, "name": "obstruction", "description": "Makes leaving difficult"}
        ]
    }