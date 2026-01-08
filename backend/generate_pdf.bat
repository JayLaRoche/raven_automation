@echo off
REM Run the PDF generation from Test_1 sheet using the FastAPI endpoint

cd /d "c:\Users\larochej3\Desktop\raven-shop-automation\backend"

echo ============================================================
echo GENERATING PDF FROM Test_1 SHEET
echo ============================================================
echo.

echo [1/2] Calling API to generate drawings...
python -c ^
"import requests; resp = requests.post('http://127.0.0.1:8000/api/drawings/Test_1/generate'); print(resp.text); print(f'Status: {resp.status_code}')"

echo.
echo [2/2] Listing generated PDFs...
echo.

if exist drawings (
    dir /b drawings\Test_1*.pdf 2>nul
    if errorlevel 1 (
        echo No PDFs found - check error above
    )
) else (
    echo Drawings folder not found
)

echo.
echo ============================================================
pause
