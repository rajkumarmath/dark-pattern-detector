# scripts/train_model.py
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import sys
import os
sys.path.append('.')

from app.services.feature_extractor import FeatureExtractor

class DarkPatternTrainer:
    def __init__(self):
        print(f"🔧 Initializing trainer with NumPy version: {np.__version__}")
        self.feature_extractor = FeatureExtractor()
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
    
    def load_data(self):
        """Load and prepare dataset"""
        print("📂 Loading dataset...")
        df = pd.read_csv('data/raw/synthetic_dataset.csv')
        df['clean_text'] = df['text'].str.lower()
        print(f"✅ Loaded {len(df)} samples")
        return df
    
    def train(self):
        """Train the model"""
        print("🚀 Starting model training...")
        
        # Load data
        df = self.load_data()
        
        # Fit TF-IDF
        print("📊 Fitting TF-IDF vectorizer...")
        self.feature_extractor.fit_tfidf(df['clean_text'])
        
        # Extract features
        print("🔍 Extracting features...")
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
        print("🤖 Training Random Forest...")
        self.classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_test)
        print("\n📊 Model Performance:")
        print(classification_report(
            y_test, y_pred,
            target_names=['none', 'forced_action', 'confirmshaming', 
                         'hidden_costs', 'interface_interference', 'obstruction']
        ))
        
        # Save model
        print("💾 Saving model...")
        os.makedirs('app/models/ml_models', exist_ok=True)
        
        model_path = 'app/models/ml_models/classifier.pkl'
        feature_path = 'app/models/ml_models/feature_extractor.pkl'
        
        joblib.dump(self.classifier, model_path)
        joblib.dump(self.feature_extractor, feature_path)
        
        # Verify save
        if os.path.exists(model_path):
            print(f"✅ Model saved to {model_path}")
            print(f"   Size: {os.path.getsize(model_path) / 1024:.2f} KB")
        else:
            print("❌ Failed to save model!")
        
        return self.classifier

if __name__ == "__main__":
    trainer = DarkPatternTrainer()
    trainer.train()
