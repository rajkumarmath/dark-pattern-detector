#!/bin/bash
echo "🚀 Starting Render build process..."

# Exit on error
set -e

# Print debug info
echo "Python version:"
python --version
echo "Pip version:"
pip --version

# Upgrade pip
pip install --upgrade pip setuptools wheel

# FIRST, install numpy with specific version (critical!)
echo "📦 Installing numpy==1.24.3..."
pip install numpy==1.24.3

# Verify numpy installation
echo "✅ NumPy installed. Version:"
python -c "import numpy; print(numpy.__version__)"

# Install scikit-learn (depends on numpy)
echo "📦 Installing scikit-learn==1.2.2..."
pip install scikit-learn==1.2.2

# Install joblib
echo "📦 Installing joblib==1.2.0..."
pip install joblib==1.2.0

# Install remaining dependencies
echo "📦 Installing remaining packages..."
pip install -r requirements.txt

# Create model directory
mkdir -p app/models/ml_models

# FORCE RETRAIN - delete old incompatible model
echo "🗑️ Removing old model files..."
rm -f app/models/ml_models/classifier.pkl
rm -f app/models/ml_models/feature_extractor.pkl

# Train fresh model with correct versions
echo "🔄 Training new model with correct NumPy version..."
python scripts/train_model.py

# Verify model was created
if [ -f "app/models/ml_models/classifier.pkl" ]; then
    echo "✅ Model trained successfully!"
else
    echo "❌ Model training failed!"
    exit 1
fi

echo "✅ Build complete! Ready to analyze screenshots."
