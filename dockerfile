FROM python:3.9-slim

# Install system dependencies including Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p app/models/ml_models

# Train model or use pre-trained
RUN python scripts/train_model.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
