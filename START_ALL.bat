@echo off
echo ╔════════════════════════════════════════════════════╗
echo ║        RAVEN SHOP AUTOMATION - STARTUP             ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo Starting servers in separate windows...
echo.

:: Start backend in new window
start "Raven Backend (Port 8000)" cmd /k "cd /d %~dp0 && START_BACKEND.bat"

:: Wait 3 seconds for backend to initialize
timeout /t 3 /nobreak >nul

:: Start frontend in new window
start "Raven Frontend (Port 3000)" cmd /k "cd /d %~dp0 && START_FRONTEND.bat"

:: Wait 5 seconds for frontend to initialize
timeout /t 5 /nobreak >nul

echo.
echo ✓ Both servers are starting in separate windows
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul

:: Open browser
start http://localhost:3000

echo.
echo ✓ Browser opened to http://localhost:3000
echo.
echo To stop servers: Close each terminal window or press Ctrl+C
pause
