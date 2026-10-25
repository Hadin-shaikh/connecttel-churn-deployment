#!/bin/bash
# ==============================================================================
# run.sh - Local execution launcher for ConnectTel Churn Prediction
# ==============================================================================
set -e

echo "Starting ConnectTel FastAPI Inference Service on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Waiting for backend to initialize..."
sleep 2

echo "Starting ConnectTel Streamlit Dashboard on port 8501..."
streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0

# Cleanup on exit
kill $BACKEND_PID
