# ✅ IMPLEMENTED: Phase 1 - Railway-ready Dockerfile
# 🔗 PLAN REF: Implementation Plan -> Phase 1 -> Docker Configuration

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
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

# Expose port for Railway
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI server
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]