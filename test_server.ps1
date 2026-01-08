# Test Server Connection Script
# This tests if the backend server is running and responding

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  RAVEN SHOP AUTOMATION - SERVER TEST" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check if port 8000 is listening
Write-Host "TEST 1: Port 8000 Status" -ForegroundColor Yellow
$netstat = netstat -an 2>$null | Select-String "8000"
if ($netstat -match "LISTENING") {
    Write-Host "  ✓ Port 8000 is LISTENING" -ForegroundColor Green
} else {
    Write-Host "  ✗ Port 8000 is NOT listening" -ForegroundColor Red
    Write-Host "    Please start the backend server first:" -ForegroundColor Yellow
    Write-Host "    cd backend" -ForegroundColor Cyan
    Write-Host "    python -m uvicorn main:app --host 0.0.0.0 --port 8000" -ForegroundColor Cyan
    exit 1
}

Write-Host ""

# Test 2: Health check endpoint
Write-Host "TEST 2: Health Check Endpoint" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.status -eq "healthy") {
        Write-Host "  ✓ Health check successful" -ForegroundColor Green
        Write-Host "    Status: $($response.status)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Unexpected response: $response" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ Health check failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 3: Frames endpoint
Write-Host "TEST 3: Frames Series Endpoint" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/frames/series" -TimeoutSec 5 -ErrorAction Stop
    if ($response.series) {
        Write-Host "  ✓ Frames endpoint responding" -ForegroundColor Green
        Write-Host "    Series count: $($response.series.Count)" -ForegroundColor Green
        Write-Host "    Series: " -ForegroundColor Cyan
        $response.series | ForEach-Object { Write-Host "      - $_" }
    } else {
        Write-Host "  ⚠ No series data returned" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Frames endpoint failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Test 4: Frames with images endpoint
Write-Host "TEST 4: Frames With Images Endpoint" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/frames/series-with-images" -TimeoutSec 5 -ErrorAction Stop
    if ($response.series -and $response.series.Count -gt 0) {
        Write-Host "  ✓ Frames with images endpoint responding" -ForegroundColor Green
        $first = $response.series[0]
        Write-Host "    First series: $($first.name)" -ForegroundColor Cyan
        Write-Host "    Has images: $($first.image_url -ne $null)" -ForegroundColor Cyan
    } else {
        Write-Host "  ⚠ No series data with images" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Frames with images endpoint failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  ✓ ALL TESTS PASSED" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open frontend: cd frontend && npm run dev" -ForegroundColor Yellow
Write-Host "  2. Visit http://localhost:3000 in your browser" -ForegroundColor Yellow
