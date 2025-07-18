# ✅ IMPLEMENTED: Phase 1 - Railway-ready Dockerfile
# 🔗 PLAN REF: Implementation Plan -> Phase 1 -> Docker Configuration

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY src/ ./src/
COPY api/ ./api/
COPY n8n-compatible-agentic-tools/ ./n8n-compatible-agentic-tools/

# Install Python dependencies
RUN pip install -e ./src/

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Railway handles port exposure dynamically

# Railway handles healthchecks via external HTTP calls

# Run the FastAPI server with Hypercorn (Railway recommended)
CMD hypercorn api.main:app --bind 0.0.0.0:$PORT