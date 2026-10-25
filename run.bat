@echo off
REM ConnectTel Churn Prediction - Windows Launcher
echo Starting ConnectTel FastAPI Backend on port 8000...
start cmd /k uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

timeout /t 2 /nobreak >nul

echo Starting ConnectTel Streamlit Frontend on port 8501...
streamlit run frontend.py
