# ✅ FIXED: Railway-ready Dockerfile with proper user permissions and uvicorn
# 🔗 PLAN REF: Implementation Plan -> Phase 1 -> Docker Configuration

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security (before copying files)
RUN useradd -m -u 1000 appuser

# Copy and install requirements first (for better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY api/ ./api/
COPY n8n-compatible-agentic-tools/ ./n8n-compatible-agentic-tools/

# Fix permissions AFTER copying files
RUN chown -R appuser:appuser /app
USER appuser

# Railway handles port exposure dynamically

# Railway handles healthchecks via external HTTP calls

# Run the FastAPI server with uvicorn (proper IPv4 binding for Railway)
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}