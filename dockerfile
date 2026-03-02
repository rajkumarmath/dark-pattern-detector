FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for OpenCV, pytesseract, and other utilities
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir scikit-learn==1.2.2 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create model directory and train model (or copy pre-trained)
RUN mkdir -p app/models/ml_models
RUN python scripts/train_model.py

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
