# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directory for models
RUN mkdir -p app/models/ml_models

# Train model on deployment (or copy pre-trained model)
RUN python scripts/train_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]