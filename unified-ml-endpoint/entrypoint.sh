#!/bin/bash
# entrypoint.sh

# Start the FastAPI app with Uvicorn
poetry run uvicorn app:app --host 0.0.0.0 --port 5000 --timeout-keep-alive 3600