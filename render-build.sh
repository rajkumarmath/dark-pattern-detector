#!/bin/bash

echo "🚀 Starting Render build..."

# Install system dependencies for pytesseract
apt-get update && apt-get install -y tesseract-ocr

# Upgrade pip and build tools
pip install --upgrade pip setuptools wheel

# Install numpy first (has wheels)
pip install numpy==1.24.3

# Install scikit-learn (will use wheel now)
pip install scikit-learn==1.2.2

# Install remaining packages
pip install -r requirements.txt

# Create model directory
mkdir -p app/models/ml_models

# Train the model (or copy pre-trained)
python scripts/train_model.py

echo "✅ Build complete!"
