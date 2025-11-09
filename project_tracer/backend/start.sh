#!/bin/bash
set -e

# Default port if not provided by platform
PORT="${PORT:-8000}"

# Ensure python path includes /app
export PYTHONPATH="/app"

echo "Starting uvicorn on 0.0.0.0:${PORT}"
exec uvicorn main:app --host 0.0.0.0 --port "${PORT}" --workers 1