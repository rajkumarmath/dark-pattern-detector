FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if absolutely necessary (e.g., for OpenCV)
# RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create model directory if it doesn't exist
RUN mkdir -p app/models/ml_models

# Train the model during build (or copy a pre-trained one)
RUN python scripts/train_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
