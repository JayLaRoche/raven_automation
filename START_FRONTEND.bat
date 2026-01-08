@echo off
TITLE Raven Frontend (Port 3000)
cd frontend
echo Starting Vite Development Server...
:: Use call to ensure script doesn't exit if npm is a batch wrapper
call npm run dev
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo CRITICAL ERROR: Frontend failed to start.
    pause
)
pause
