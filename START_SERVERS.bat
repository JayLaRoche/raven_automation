@echo off
REM Start Raven Shop Drawing Servers
REM This batch file starts both backend and frontend servers

echo.
echo ========================================
echo Raven Shop Drawing - Server Startup
echo ========================================
echo.

REM Start Backend in a new window
echo Starting Backend on port 8000...
start "Backend - FastAPI" cmd /k "cd C:\Users\larochej3\Desktop\raven-shop-automation\backend && uvicorn main:app --reload --host 0.0.0.0"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start Frontend in a new window
echo Starting Frontend on port 3000...
start "Frontend - React" cmd /k "cd C:\Users\larochej3\Desktop\raven-shop-automation\frontend && npm run dev"

REM Give it a moment to start
timeout /t 2 /nobreak

echo.
echo ========================================
echo Servers Starting Up...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two new windows will open with the servers.
echo You can close this window.
echo.
pause
