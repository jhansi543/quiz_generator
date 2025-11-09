# Use a small Python base
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy only what we need first (helps Docker cache)
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Ensure start script is executable
RUN chmod +x /app/start.sh

# Use the PORT env var that Vercel will set; default to 8000 locally if missing
EXPOSE 8000

# Start the app (start.sh will use $PORT if available)
CMD ["./start.sh"]