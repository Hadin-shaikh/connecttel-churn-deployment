#!/bin/bash
# Capture Render's assigned port (defaults to 10000)
RENDER_PORT="${PORT:-10000}"

# Start FastAPI on a strict internal port (8000)
PORT=8000 uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on the public Render port, pointing it to the internal FastAPI server
API_URL="http://localhost:8000" streamlit run frontend.py --server.port $RENDER_PORT --server.address 0.0.0.0
