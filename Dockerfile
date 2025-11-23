# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend /app/backend

# Set working directory to backend
WORKDIR /app/backend

# Expose port (Railway will use the PORT env variable)
EXPOSE 8000

# Start command
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
