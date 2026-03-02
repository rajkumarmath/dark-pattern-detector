# scripts/train_model.py
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from pathlib import Path
import sys
sys.path.append('.')

from app.services.feature_extractor import FeatureExtractor

class DarkPatternTrainer:
    """
    Why Random Forest:
    - Works well with mixed feature types
    - Handles non-linear relationships
    - Provides feature importance (explainability)
    - Fast training on laptop
    """
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced classes
        )
    
    def load_data(self):
        """Load and prepare dataset"""
        df = pd.read_csv('data/raw/synthetic_dataset.csv')
        
        # Clean text
        df['clean_text'] = df['text'].str.lower()
        
        return df
    
    def train(self):
        """Train the model"""
        # Load data
        df = self.load_data()
        
        # Fit TF-IDF on all texts
        self.feature_extractor.fit_tfidf(df['clean_text'])
        
        # Extract features for all samples
        X_features = []
        for text in df['clean_text']:
            features = self.feature_extractor.extract_features(text)
            X_features.append(features)
        
        X = np.array(X_features)
        y = df['pattern_type'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train
        self.classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_test)
        print("\n📊 Model Performance:")
        print(classification_report(
            y_test, y_pred,
            target_names=['none', 'forced_action', 'confirmshaming', 
                         'hidden_costs', 'interface_interference', 'obstruction']
        ))
        
        # Save model and vectorizer
        Path('app/models/ml_models').mkdir(parents=True, exist_ok=True)
        joblib.dump(self.classifier, 'app/models/ml_models/classifier.pkl')
        joblib.dump(self.feature_extractor, 'app/models/ml_models/feature_extractor.pkl')
        
        print("✅ Model saved to app/models/ml_models/")
        
        return self.classifier

if __name__ == "__main__":
    trainer = DarkPatternTrainer()
    trainer.train()