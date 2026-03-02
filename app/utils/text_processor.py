# app/utils/text_processor.py
import re
from typing import List

class TextProcessor:
    """
    Clean and preprocess text for analysis
    """
    
    def __init__(self):
        # Common patterns to clean
        self.clean_patterns = [
            (r'\s+', ' '),  # Multiple spaces to single space
            (r'[^\w\s\.\?\!\,\$\€\£]', ''),  # Remove special chars but keep punctuation and currency
            (r'^\s+|\s+$', '')  # Trim whitespace
        ]
    
    def clean(self, text: str) -> str:
        """
        Clean and normalize text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Apply cleaning patterns
        for pattern, replacement in self.clean_patterns:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        """
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def contains_currency(self, text: str) -> bool:
        """
        Check if text contains currency symbols
        """
        currency_pattern = r'[\$\€\£]|\b(?:dollars?|euros?|pounds?)\b'
        return bool(re.search(currency_pattern, text.lower()))
    
    def extract_numbers(self, text: str) -> List[float]:
        """
        Extract all numbers from text
        """
        numbers = re.findall(r'\d+\.?\d*', text)
        return [float(n) for n in numbers]