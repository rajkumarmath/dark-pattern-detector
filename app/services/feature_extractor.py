# app/services/feature_extractor.py
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np

class FeatureExtractor:
    """
    Why TF-IDF + Heuristics:
    - TF-IDF captures important words/phrases
    - Heuristics capture patterns TF-IDF misses
    - Combined features improve accuracy
    """
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(
            max_features=500,  # Keep features manageable
            ngram_range=(1, 3),  # Capture phrases like "no thanks"
            stop_words='english'
        )
        
        # Pattern-specific keywords
        self.pattern_keywords = {
            1: ['must', 'required', 'forced', 'only way', 'need to'],  # Forced Action
            2: ['no thanks', 'i prefer', 'skip', 'pass on'],  # Confirmshaming
            3: ['fee', 'additional', 'plus', 'extra', 'handling'],  # Hidden Costs
            4: ['tiny', 'hidden', 'small', 'barely visible'],  # Interface Interference
            5: ['call', 'form', 'contact', 'wait', 'office hours']  # Obstruction
        }
    
    def extract_heuristic_features(self, text: str) -> np.array:
        """
        Extract hand-crafted features based on dark pattern indicators
        """
        text_lower = text.lower()
        features = []
        
        # Feature 1: Count of manipulative words per pattern
        for pattern_id, keywords in self.pattern_keywords.items():
            count = sum(text_lower.count(kw) for kw in keywords)
            features.append(count)
        
        # Feature 2: Presence of urgency words
        urgency_words = ['now', 'today', 'immediately', 'limited']
        urgency_score = sum(text_lower.count(w) for w in urgency_words)
        features.append(urgency_score)
        
        # Feature 3: Question marks (potential confirmshaming)
        features.append(text.count('?'))
        
        # Feature 4: Exclamation marks (emotional manipulation)
        features.append(text.count('!'))
        
        # Feature 5: Currency symbols (payment context)
        features.append(len(re.findall(r'[$£€]', text)))
        
        return np.array(features)
    
    def fit_tfidf(self, texts):
        """Fit TF-IDF on training texts"""
        self.tfidf.fit(texts)
    
    def extract_features(self, text: str) -> np.array:
        """
        Combine TF-IDF and heuristic features
        """
        # Get TF-IDF features
        tfidf_features = self.tfidf.transform([text]).toarray()[0]
        
        # Get heuristic features
        heuristic_features = self.extract_heuristic_features(text)
        
        # Combine
        combined = np.concatenate([tfidf_features, heuristic_features])
        
        return combined
    
    def get_manipulative_phrases(self, text: str, pattern_type: int) -> list:
        """
        Extract manipulative phrases from text based on detected pattern
        """
        text_lower = text.lower()
        found_phrases = []
        
        # Get keywords for the detected pattern
        keywords = self.pattern_keywords.get(pattern_type, [])
        
        # Find which keywords appear in the text
        for keyword in keywords:
            if keyword in text_lower:
                found_phrases.append(keyword)
        
        # Also look for pattern-specific indicators
        if pattern_type == 3:  # Hidden costs
            if '$' in text or '€' in text or '£' in text:
                found_phrases.append('currency_symbol')
        
        # For forced action, look for must/required patterns
        if pattern_type == 1:
            if 'must' in text_lower or 'required' in text_lower:
                found_phrases.append('requirement_language')
        
        return found_phrases[:5]  # Return top 5 phrases