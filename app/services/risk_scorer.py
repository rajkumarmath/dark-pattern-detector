# app/services/risk_scorer.py
import re
from typing import Dict, Any, List

class RiskScorer:
    """
    Calculates risk score 0-100 based on multiple factors
    """
    
    def __init__(self):
        # Base severity by pattern type (adjusted for better accuracy)
        self.pattern_severity = {
            0: 0,    # No pattern
            1: 65,   # Forced Action (medium-high)
            2: 40,   # Confirmshaming (medium-low)
            3: 70,   # Hidden Costs (high - but reduced from 85)
            4: 55,   # Interface Interference (medium)
            5: 75    # Obstruction (high - time waste)
        }
        
        # Context multipliers
        self.context_weights = {
            'checkout': 1.3,      # Financial decisions
            'signup': 1.1,         # Data privacy
            'cancellation': 1.4,   # Retention tactics
            'default': 1.0
        }
    
    def calculate_intensity(self, text: str, pattern_type: int, 
                           manipulative_phrases: List[str]) -> float:
        """
        Calculate how intense/manipulative the pattern is
        """
        text_lower = text.lower()
        
        # Factor 1: Density of manipulative phrases
        if manipulative_phrases:
            words = text.split()
            word_count = len(words) if words else 1
            phrase_density = sum(
                text_lower.count(phrase) for phrase in manipulative_phrases
            ) / word_count
        else:
            phrase_density = 0
        
        # Factor 2: Emotional language intensity
        emotional_markers = ['!', '?', 'urgent', 'limited', 'expires', 'now', 'today']
        emotional_score = sum(text_lower.count(m) for m in emotional_markers) / 10
        
        # Factor 3: Pattern-specific intensity
        if pattern_type == 3:  # Hidden costs
            # Check for vague vs specific amounts
            has_specific = bool(re.search(r'\$\d+', text))
            intensity = 1.2 if has_specific else 0.8
        elif pattern_type == 5:  # Obstruction
            # More steps = higher intensity
            steps = len(re.findall(r'step|form|call|email|print|mail', text_lower))
            intensity = min(1.0 + steps * 0.1, 1.5)
        else:
            intensity = 1.0
        
        # Combine factors (normalize to 0-1.5 range)
        raw_intensity = (phrase_density * 2 + emotional_score) * intensity
        return min(float(raw_intensity), 1.5)
    
    def detect_context(self, text: str) -> str:
        """
        Detect where this pattern appears
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['checkout', 'pay', 'cart', 'buy', 'purchase', 'order']):
            return 'checkout'
        elif any(word in text_lower for word in ['sign', 'register', 'join', 'create account', 'newsletter']):
            return 'signup'
        elif any(word in text_lower for word in ['cancel', 'unsubscribe', 'delete', 'remove', 'close account']):
            return 'cancellation'
        else:
            return 'default'
    
    def calculate_risk(self, text: str, pattern_type: int, 
                      manipulative_phrases: List[str]) -> Dict[str, Any]:
        """
        Calculate final risk score with breakdown
        """
        # Get base score
        base_score = self.pattern_severity.get(pattern_type, 50)
        
        if pattern_type == 0:
            return {
                'score': 0.0,
                'breakdown': {
                    'base': 0.0,
                    'intensity_multiplier': 0.0,
                    'context_multiplier': 0.0,
                    'context_detected': 'none',
                    'final': 0.0
                },
                'level': 'none'
            }
        
        # Calculate multipliers
        context = self.detect_context(text)
        context_multiplier = self.context_weights.get(context, 1.0)
        
        intensity = self.calculate_intensity(text, pattern_type, manipulative_phrases)
        
        # Apply multipliers
        final_score = base_score * context_multiplier * intensity
        
        # Cap at 100
        final_score = min(final_score, 100.0)
        
        # Determine risk level
        if final_score < 30:
            level = 'low'
        elif final_score < 60:
            level = 'medium'
        else:
            level = 'high'
        
        # Return with all required fields
        return {
            'score': round(final_score, 1),
            'breakdown': {
                'base': float(base_score),
                'intensity_multiplier': round(float(intensity), 2),
                'context_multiplier': float(context_multiplier),
                'context_detected': context,
                'final': round(float(final_score), 1)
            },
            'level': level
        }