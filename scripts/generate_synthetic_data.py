# scripts/generate_synthetic_data.py
import csv
import random
from pathlib import Path
from dataclasses import dataclass  # Add this import
from typing import List, Optional   # Add this import

# Define the dataclass RIGHT HERE in the same file
@dataclass
class DarkPatternSample:
    text: str
    pattern_type: int  # 0-6 as defined
    pattern_name: str
    source_url: Optional[str]
    manipulative_phrases: List[str]
    context: str  # Where it appears (checkout, signup, etc.)

class SyntheticDataGenerator:
    """
    Why: We need diverse examples of each dark pattern type
    to train a robust classifier.
    """
    
    def __init__(self):
        self.patterns = {
            0: {  # No Dark Pattern
                'templates': [
                    "Sign up for our newsletter to receive updates",
                    "Click here to complete your purchase",
                    "Enter your email to create an account",
                    "Would you like to save your progress?",
                    "Choose your preferred settings"
                ],
                'phrases': []
            },
            1: {  # Forced Action
                'templates': [
                    "You must accept cookies to continue browsing",
                    "Sign up now to read this article",
                    "Download our app to see the full content",
                    "Create an account to view prices",
                    "Please login to access this feature"
                ],
                'phrases': ['must', 'required', 'only way', 'forced', 'need to']
            },
            2: {  # Confirmshaming
                'templates': [
                    "No thanks, I don't want to save money",
                    "I prefer paying full price",
                    "Skip and continue with basic features",
                    "No, I don't want to support creators",
                    "I'll pass on this exclusive offer"
                ],
                'phrases': ['no thanks', 'i prefer', 'skip and', 'pass on']
            },
            3: {  # Hidden Costs
                'templates': [
                    "Total: $49.99 plus handling fee",
                    "Service fee of $15 will be added",
                    "Convenience fee applies at checkout",
                    "Additional processing charges apply",
                    f"Total: ${random.randint(10,100)}.00 plus taxes and fees"
                ],
                'phrases': ['fee', 'additional', 'plus', 'hidden', 'extra charges']
            },
            4: {  # Interface Interference
                'templates': [
                    "No, I don't want this amazing deal (tiny link at bottom)",
                    "Unsubscribe (small text at bottom of email)",
                    "Cancel subscription (hidden in account settings)",
                    "Click here to decline (barely visible button)",
                    "Skip this step (link hidden in fine print)"
                ],
                'phrases': ['tiny', 'hidden', 'difficult', 'small', 'barely visible']
            },
            5: {  # Obstruction
                'templates': [
                    "To cancel, please call between 9-5 M-F",
                    "Fill this 10-page form to delete account",
                    "Contact support for cancellation (24h response time)",
                    "Please print and mail this form to cancel",
                    "Visit our office during business hours to close account"
                ],
                'phrases': ['call', 'form', 'contact', 'wait', 'office hours', 'mail']
            }
        }
    
    def generate_sample(self, pattern_type: int) -> DarkPatternSample:
        """Generate one synthetic sample"""
        pattern = self.patterns[pattern_type]
        text = random.choice(pattern['templates'])
        
        # Add variations for hidden costs
        if pattern_type == 3:  # Hidden costs - add random amounts
            if '$' in text:
                amount = random.randint(5, 50)
                text = text.replace('$49.99', f'${amount}.99')
                text = text.replace('$15', f'${random.randint(5,25)}')
        
        # Add variations for obstruction
        if pattern_type == 5:  # Obstruction - vary the time
            if '24h' in text:
                hours = random.choice(['24h', '48h', '3-5 business days'])
                text = text.replace('24h', hours)
        
        return DarkPatternSample(
            text=text,
            pattern_type=pattern_type,
            pattern_name=['none', 'forced_action', 'confirmshaming', 
                         'hidden_costs', 'interface_interference', 'obstruction'][pattern_type],
            source_url='synthetic',
            manipulative_phrases=pattern['phrases'],
            context='synthetic_training'
        )
    
    def generate_dataset(self, samples_per_class: int = 200):
        """Generate balanced dataset"""
        print(f"🚀 Generating {samples_per_class} samples per class...")
        dataset = []
        
        for pattern_type in range(6):  # 0-5
            print(f"  Generating class {pattern_type}...")
            for _ in range(samples_per_class):
                dataset.append(self.generate_sample(pattern_type))
        
        # Save to CSV
        csv_path = 'data/raw/synthetic_dataset.csv'
        print(f"💾 Saving to {csv_path}...")
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['text', 'pattern_type', 'pattern_name', 'manipulative_phrases'])
            for sample in dataset:
                writer.writerow([
                    sample.text, 
                    sample.pattern_type,
                    sample.pattern_name,
                    '|'.join(sample.manipulative_phrases)
                ])
        
        print(f"✅ Generated {len(dataset)} samples successfully!")
        print(f"📁 File saved at: {os.path.abspath(csv_path)}")
        return dataset

if __name__ == "__main__":
    import os  # Add this import for the path display
    generator = SyntheticDataGenerator()
    generator.generate_dataset(200)  # 1200 total samples