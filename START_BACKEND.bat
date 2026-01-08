@echo off
TITLE Raven Backend (Port 8000)
cd backend
echo Starting FastAPI Backend...
:: Use call to ensure script doesn't exit if uvicorn is a batch wrapper
call uvicorn main:app --reload
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo CRITICAL ERROR: Backend failed to start.
    pause
)
pause
