# Dockerfile for Luxion Omega V9 v4.4
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the complete Luxion system
COPY luxion_v9_complete_single_file_v4.py .

# Expose port
EXPOSE 8000

# Run the server
CMD ["uvicorn", "luxion_v9_complete_single_file_v4:app", "--host", "0.0.0.0", "--port", "8000"]
