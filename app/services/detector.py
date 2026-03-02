# app/services/detector.py
import joblib
from typing import Dict, Any, Optional
import numpy as np
from pathlib import Path

from app.core.config import settings
from app.models.schemas import DetectionResponse, RiskScore, EthicalSuggestion
from app.services.feature_extractor import FeatureExtractor
from app.services.risk_scorer import RiskScorer
from app.services.explainer import Explainer
from app.services.ethics_suggester import EthicsSuggester
from app.utils.text_processor import TextProcessor

class DarkPatternDetector:
    """
    Main orchestrator for dark pattern detection
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.risk_scorer = RiskScorer()
        self.explainer = Explainer()
        self.ethics_suggester = EthicsSuggester()
        
        # Load ML models
        self.load_models()
    
    def load_models(self):
        """Load trained ML models"""
        try:
            self.classifier = joblib.load(settings.MODEL_PATH)
            self.feature_extractor = joblib.load(settings.FEATURE_EXTRACTOR_PATH)
            self.models_loaded = True
            print("✅ Models loaded successfully")
        except FileNotFoundError as e:
            print(f"⚠️ Models not found: {e}. Using rule-based fallback.")
            self.models_loaded = False
        except Exception as e:
            print(f"⚠️ Error loading models: {e}. Using rule-based fallback.")
            self.models_loaded = False
    
    def extract_text_from_url(self, url: str) -> str:
        """
        Extract text content from URL
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit length
        except Exception as e:
            raise ValueError(f"Failed to extract text from URL: {str(e)}")
    
    def predict_fallback(self, text: str) -> Dict[str, Any]:
        """
        Rule-based fallback when ML model isn't available
        """
        text_lower = text.lower()
        
        # First check for CLEAN DESIGN indicators (NO dark patterns)
        clean_indicators = [
            'welcome', 'choose', 'preferences', 'optional', 'feel free',
            'would you like', 'select', 'your choice', 'pick', 'decide',
            'settings', 'customize', 'prefer', 'interested'
        ]
        
        clean_score = sum(2 for ind in clean_indicators if ind in text_lower)
        
        # Enhanced pattern keywords with weights
        pattern_keywords = {
            1: {
                'words': ['must', 'required', 'forced', 'need to', 'have to', 'create an account', 'sign up', 'login', 'register', 'account required', 'continue', 'proceed'],
                'phrases': ['you must', 'is required', 'need to create', 'sign up to continue', 'login to view', 'create account to', 'must create', 'required to continue'],
                'weight': 2
            },
            2: {
                'words': ['no thanks', 'i prefer', 'skip', 'pass', 'not interested'],
                'phrases': ["don't want to", "prefer to", "no thank you", "i'll pass"],
                'weight': 3
            },
            3: {
                'words': ['fee', 'additional', 'plus', 'extra', 'handling', 'processing', 'convenience', 'service charge'],
                'phrases': ['plus fees', 'additional charge', 'service fee', 'handling fee', 'processing fee'],
                'weight': 3
            },
            4: {
                'words': ['tiny', 'hidden', 'small', 'barely', 'difficult', 'hard to', 'unsubscribe', 'cancel'],
                'phrases': ['tiny link', 'hidden button', 'small print', 'barely visible', 'click here to unsubscribe'],
                'weight': 2
            },
            5: {
                'words': ['call', 'form', 'contact', 'wait', 'office hours', 'business hours', 'mail', 'print'],
                'phrases': ['call us', 'fill form', 'contact support', 'during business hours', 'print and mail'],
                'weight': 2
            }
        }
        
        # Calculate scores for each pattern
        scores = {}
        for pattern_id, keywords in pattern_keywords.items():
            score = 0
            # Check individual words
            for word in keywords['words']:
                if word in text_lower:
                    score += keywords.get('weight', 1)
            # Check phrases (higher weight)
            for phrase in keywords['phrases']:
                if phrase in text_lower:
                    score += keywords.get('weight', 1) * 2
            scores[pattern_id] = score
        
        # If clean indicators present AND low pattern scores, return none
        if clean_score > 0 and max(scores.values()) < 3:
            return {'pattern_type': 0, 'confidence': 0.85}
        
        # If no patterns found, return none
        if max(scores.values()) == 0:
            return {'pattern_type': 0, 'confidence': 1.0}
        
        # Get pattern with highest score
        predicted = max(scores, key=scores.get)
        total_score = sum(scores.values())
        confidence = scores[predicted] / total_score if total_score > 0 else 0
        
        return {
            'pattern_type': predicted,
            'confidence': min(confidence, 0.9)
        }
    
    def detect(self, text: Optional[str] = None, url: Optional[str] = None) -> DetectionResponse:
        """
        Main detection pipeline
        """
        try:
            # Input validation
            if not text and not url:
                raise ValueError("Either text or URL must be provided")
            
            # Get text content
            if url:
                text = self.extract_text_from_url(url)
            
            if not text:
                raise ValueError("No text content to analyze")
            
            # Clean text
            clean_text = self.text_processor.clean(text)
            
            # Predict pattern
            if self.models_loaded:
                features = self.feature_extractor.extract_features(clean_text)
                prediction = self.classifier.predict([features])[0]
                proba = self.classifier.predict_proba([features])[0]
                confidence = float(max(proba))
            else:
                fallback = self.predict_fallback(clean_text)
                prediction = fallback['pattern_type']
                confidence = fallback['confidence']
            
            # Get manipulative phrases
            if self.models_loaded:
                manipulative_phrases = self.feature_extractor.get_manipulative_phrases(clean_text, prediction)
            else:
                # Simple keyword extraction for fallback
                phrase_map = {
                    1: ['must', 'required', 'forced', 'need to'],
                    2: ['no thanks', 'i prefer', 'skip'],
                    3: ['fee', 'additional', 'plus', 'handling'],
                    4: ['tiny', 'hidden', 'unsubscribe'],
                    5: ['call', 'contact', 'form', 'business hours']
                }
                keywords = phrase_map.get(prediction, [])
                manipulative_phrases = [kw for kw in keywords if kw in clean_text.lower()]
            
            # Calculate risk score
            risk_result = self.risk_scorer.calculate_risk(
                clean_text, 
                prediction,
                manipulative_phrases
            )
            
            # Generate explanation
            explanation = self.explainer.generate_explanation(
                prediction,
                risk_result['score'],
                manipulative_phrases
            )
            
            # Get ethical suggestions
            context = risk_result['breakdown']['context_detected']
            ethical_suggestion = self.ethics_suggester.suggest_corrections(prediction, context)
            
            # Pattern names mapping
            pattern_names = ['none', 'forced_action', 'confirmshaming', 
                           'hidden_costs', 'interface_interference', 'obstruction']
            
            # Create response
            return DetectionResponse(
                pattern_type=prediction,
                pattern_name=pattern_names[prediction],
                risk_score=RiskScore(**risk_result),
                explanation=explanation,
                ethical_recommendation=EthicalSuggestion(**ethical_suggestion),
                confidence=confidence
            )
            
        except Exception as e:
            print(f"🔥 Error in detect: {str(e)}")
            import traceback
            traceback.print_exc()
            raise