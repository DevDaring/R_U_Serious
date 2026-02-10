FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Copy data directories (bust cache to ensure fresh CSV files)
ARG CACHEBUST=1
COPY data/csv/ ./data/csv/
COPY data/mct_images/ ./data/mct_images/

# Copy avatar and character images (persistent user-created content)
COPY data/media/avatars/ ./data/media/avatars/
COPY data/media/characters/ ./data/media/characters/
COPY data/media/generated_images/ ./data/media/generated_images/

# Create remaining media directories (ephemeral - will reset on restart)
RUN mkdir -p data/media/generated_videos \
    data/media/generated_videos \
    data/media/audio \
    data/media/uploads \
    data/media/temp

# Create secrets directory (Cloud Run will use default service account)
RUN mkdir -p secrets

# Expose Cloud Run port
EXPOSE 8080

# Start application with timeout configured for Cloud Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--timeout-keep-alive", "300"]
