# app/services/multimodal_detector.py
from typing import Optional, Dict, Any
from app.services.detector import DarkPatternDetector
from app.services.screenshot_analyzer import ScreenshotAnalyzer
from app.services.solution_provider import SolutionProvider
from app.services.risk_scorer import RiskScorer
from app.services.explainer import Explainer
import os

class MultiModalDetector:
    """
    Unified detector that handles text, URLs, and screenshots
    """
    
    def __init__(self):
        self.text_detector = DarkPatternDetector()
        self.screenshot_analyzer = ScreenshotAnalyzer()
        self.solution_provider = SolutionProvider()
        self.risk_scorer = RiskScorer()
        self.explainer = Explainer()
    
    def detect_from_text(self, text: str) -> Dict:
        """Analyze text input"""
        return self.text_detector.detect(text=text).dict()
    
    def detect_from_url(self, url: str) -> Dict:
        """Analyze URL input"""
        return self.text_detector.detect(url=url).dict()
    
    def detect_from_screenshot(self, image_path: str) -> Dict:
        """Analyze screenshot input"""
        if not os.path.exists(image_path):
            raise ValueError(f"Image not found: {image_path}")
        
        # Analyze screenshot
        visual_results = self.screenshot_analyzer.analyze_screenshot(image_path)
        
        # Extract text from screenshot for text analysis
        extracted_text = visual_results.get("text_extracted", "")
        
        # Run text analysis on extracted text
        text_results = {}
        if extracted_text:
            try:
                text_results = self.text_detector.detect(text=extracted_text).dict()
            except Exception as e:
                text_results = {"error": f"Text analysis failed: {str(e)}"}
        
        # Combine results
        combined_results = {
            "input_type": "screenshot",
            "image_path": image_path,
            "visual_analysis": visual_results,
            "text_analysis": text_results if text_results else None,
            "detected_patterns": []
        }
        
        # Determine if visual patterns indicate dark patterns
        visual_risk = visual_results.get("overall_visual_risk", "low")
        
        # Check for specific visual dark patterns
        visual_patterns = visual_results.get("visual_patterns", {})
        for pattern_name, pattern_data in visual_patterns.items():
            if pattern_data.get("result", {}).get("detected", False):
                combined_results["detected_patterns"].append({
                    "type": "visual",
                    "name": pattern_name,
                    "description": pattern_data.get("description", ""),
                    "details": pattern_data.get("result", {})
                })
        
        # Add text-based patterns if found
        if text_results and text_results.get("pattern_type", 0) != 0:
            combined_results["detected_patterns"].append({
                "type": "text",
                "name": text_results.get("pattern_name", ""),
                "pattern_type": text_results.get("pattern_type"),
                "risk_score": text_results.get("risk_score"),
                "explanation": text_results.get("explanation")
            })
        
        # Calculate overall risk
        risks = [visual_risk]
        if text_results and "risk_score" in text_results:
            text_risk = text_results["risk_score"].get("level", "low")
            risks.append(text_risk)
        
        if "high" in risks:
            combined_results["overall_risk"] = "high"
        elif "medium" in risks:
            combined_results["overall_risk"] = "medium"
        else:
            combined_results["overall_risk"] = "low"
        
        return combined_results
    
    def get_solutions(self, detection_result: Dict) -> Dict:
        """Get solutions for detected patterns"""
        pattern_type = 0
        context = "default"
        
        # Extract pattern type from result
        if "pattern_type" in detection_result:
            pattern_type = detection_result["pattern_type"]
        elif "detected_patterns" in detection_result:
            # For multimodal results, use the first detected pattern
            for pattern in detection_result["detected_patterns"]:
                if pattern.get("type") == "text":
                    pattern_type = pattern.get("pattern_type", 0)
                    break
        
        return self.solution_provider.get_solutions(pattern_type, context)
    
    def generate_improvement_report(self, detection_result: Dict) -> str:
        """Generate comprehensive improvement report"""
        return self.solution_provider.generate_report(detection_result)