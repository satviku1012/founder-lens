FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Set Python path to find the 'backend' module
ENV PYTHONPATH=/app

# Run server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
