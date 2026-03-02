# app/services/screenshot_analyzer.py
import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Dict, List, Optional
import re

# Configure Tesseract path (Windows)
import platform
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenshotAnalyzer:
    """
    Analyze screenshots to detect visual dark patterns
    """
    
    def __init__(self):
        self.visual_patterns = {
            "tiny_buttons": {
                "description": "Important buttons are unusually small",
                "detect": self.detect_tiny_buttons
            },
            "hidden_elements": {
                "description": "Elements hidden in low contrast",
                "detect": self.detect_hidden_elements
            },
            "misleading_contrast": {
                "description": "Using color to manipulate choices",
                "detect": self.detect_misleading_contrast
            },
            "pre_selected": {
                "description": "Options pre-selected against user interest",
                "detect": self.detect_pre_selected
            }
        }
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract all text from screenshot using OCR"""
        try:
            # Open image
            image = Image.open(image_path)
            
            # Extract text
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"❌ OCR Error: {e}")
            return ""
    
    def detect_tiny_buttons(self, image_path: str) -> Dict:
        """Detect unusually small buttons"""
        try:
            # Read image
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Find contours (potential buttons)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Get image dimensions
            height, width = img.shape[:2]
            total_area = height * width
            
            tiny_buttons = []
            for contour in contours:
                area = cv2.contourArea(contour)
                # If area is less than 1% of screen and looks like button
                if area < total_area * 0.01 and area > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    # Button-like aspect ratio
                    if 2 < aspect_ratio < 6:
                        tiny_buttons.append({
                            "position": (x, y),
                            "size": f"{w}x{h}",
                            "area_ratio": f"{(area/total_area*100):.2f}%"
                        })
            
            return {
                "detected": len(tiny_buttons) > 0,
                "count": len(tiny_buttons),
                "buttons": tiny_buttons,
                "risk": "high" if len(tiny_buttons) > 2 else "medium" if len(tiny_buttons) > 0 else "low"
            }
        except Exception as e:
            return {"detected": False, "error": str(e)}
    
    def detect_hidden_elements(self, image_path: str) -> Dict:
        """Detect low-contrast or hidden elements"""
        try:
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Calculate contrast
            contrast = gray.std()
            
            # Look for text with low contrast
            text_regions = []
            
            # Use OCR to find text positions
            import pytesseract
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            
            low_contrast_text = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30:  # Valid text
                    text = data['text'][i]
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    
                    # Check contrast in this region
                    roi = gray[y:y+h, x:x+w]
                    if roi.size > 0:
                        region_contrast = roi.std()
                        if region_contrast < 30:  # Low contrast
                            low_contrast_text.append({
                                "text": text,
                                "position": (x, y),
                                "contrast": float(region_contrast)
                            })
            
            return {
                "detected": len(low_contrast_text) > 0,
                "low_contrast_elements": low_contrast_text,
                "overall_contrast": float(contrast),
                "risk": "high" if len(low_contrast_text) > 3 else "medium" if len(low_contrast_text) > 0 else "low"
            }
        except Exception as e:
            return {"detected": False, "error": str(e)}
    
    def detect_misleading_contrast(self, image_path: str) -> Dict:
        """Detect if important options are de-emphasized"""
        try:
            img = cv2.imread(image_path)
            
            # Convert to HSV for color analysis
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Look for gray/dimmed text (possible de-emphasized options)
            # Gray typically has low saturation
            saturation = hsv[:, :, 1]
            low_sat_mask = saturation < 50
            
            # Look for bright/highlighted options (emphasized)
            brightness = hsv[:, :, 2]
            high_bright_mask = brightness > 200
            
            gray_percentage = np.sum(low_sat_mask) / low_sat_mask.size * 100
            bright_percentage = np.sum(high_bright_mask) / high_bright_mask.size * 100
            
            return {
                "detected": gray_percentage > 30 or bright_percentage < 10,
                "analysis": {
                    "de_emphasized_area": f"{gray_percentage:.1f}%",
                    "emphasized_area": f"{bright_percentage:.1f}%"
                },
                "risk": "high" if gray_percentage > 50 else "medium" if gray_percentage > 30 else "low"
            }
        except Exception as e:
            return {"detected": False, "error": str(e)}
    
    def detect_pre_selected(self, image_path: str) -> Dict:
        """Detect pre-selected checkboxes/options"""
        try:
            img = cv2.imread(image_path)
            
            # Look for checkboxes with ticks/marks
            # This is simplified - would need more sophisticated detection
            
            # Look for text indicating pre-selection
            text = self.extract_text_from_image(image_path)
            text_lower = text.lower()
            
            pre_select_indicators = [
                "pre-selected", "preselected", "default", 
                "recommended", "popular", "best choice"
            ]
            
            found = [ind for ind in pre_select_indicators if ind in text_lower]
            
            return {
                "detected": len(found) > 0,
                "indicators": found,
                "risk": "high" if "pre-selected" in text_lower else "medium" if found else "low"
            }
        except Exception as e:
            return {"detected": False, "error": str(e)}
    
    def analyze_screenshot(self, image_path: str) -> Dict:
        """Complete screenshot analysis"""
        print(f"🔍 Analyzing screenshot: {image_path}")
        
        # Extract text from image
        extracted_text = self.extract_text_from_image(image_path)
        
        results = {
            "text_extracted": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
            "visual_patterns": {}
        }
        
        # Run all visual pattern detectors
        for pattern_name, detector in self.visual_patterns.items():
            try:
                result = detector["detect"](image_path)
                results["visual_patterns"][pattern_name] = {
                    "description": detector["description"],
                    "result": result
                }
            except Exception as e:
                results["visual_patterns"][pattern_name] = {
                    "error": str(e)
                }
        
        # Calculate overall visual risk
        risks = []
        for pattern in results["visual_patterns"].values():
            if "result" in pattern and "risk" in pattern["result"]:
                risks.append(pattern["result"]["risk"])
        
        if "high" in risks:
            overall_risk = "high"
        elif "medium" in risks:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        results["overall_visual_risk"] = overall_risk
        
        return results