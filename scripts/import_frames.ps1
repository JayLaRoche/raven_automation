# Frame Images Import and Rename Script
# Copies PNG files from source folder and renames them to match backend expectations
# Series_86_a.PNG -> series_86_HEAD.png
# Series_86_b.PNG -> series_86_SILL.png
# Series_86_c.PNG -> series_86_JAMB.png

param(
    [string]$SourceDir = $null,
    [string]$DestDir = "backend\static\frames"
)

# If no source specified, try frame_library first, then Upwork folder
if (-not $SourceDir) {
    $frameLibraryPath = "backend\frame_library"
    $upworkPath = "C:\Users\larochej3\Desktop\Upwork\Raven Glass Project\frames"
    
    # Try frame_library first (relative path)
    if (-not [System.IO.Path]::IsPathRooted($frameLibraryPath)) {
        $absFrameLibPath = Join-Path (Get-Location) $frameLibraryPath
    } else {
        $absFrameLibPath = $frameLibraryPath
    }
    
    if (Test-Path $absFrameLibPath -PathType Container) {
        $SourceDir = $absFrameLibPath
    } elseif (Test-Path $upworkPath -PathType Container) {
        $SourceDir = $upworkPath
    }
}

# Resolve destination to absolute path if relative
if (-not [System.IO.Path]::IsPathRooted($DestDir)) {
    $DestDir = Join-Path (Get-Location) $DestDir
}

Write-Host ""
Write-Host "Frame Images Import and Rename Script" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Validate source directory exists
if (-not (Test-Path $SourceDir -PathType Container)) {
    Write-Host "ERROR: Source directory not found!" -ForegroundColor Red
    Write-Host "Expected: $SourceDir"
    Write-Host ""
    exit 1
}

Write-Host "Source directory: $SourceDir" -ForegroundColor Green
Write-Host "Destination directory: $DestDir" -ForegroundColor Green
Write-Host ""

# Create destination directory if it doesn't exist
if (-not (Test-Path $DestDir -PathType Container)) {
    Write-Host "Creating destination directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
}

Write-Host ""
Write-Host "Scanning for PNG files..." -ForegroundColor Yellow
Write-Host ""

# Get all PNG files in source directory
$pngFiles = Get-ChildItem -Path $SourceDir -Filter "*.PNG" -File

if ($pngFiles.Count -eq 0) {
    Write-Host "No PNG files found in source directory" -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($pngFiles.Count) PNG files" -ForegroundColor Cyan
Write-Host ""

$importedCount = 0
$skippedCount = 0

# Process each PNG file
foreach ($file in $pngFiles) {
    $originalName = $file.Name
    $baseName = $file.BaseName
    
    # Extract the view type suffix and series number
    # Expected format: Series_86_a, Series_86_b, Series_86_c, etc.
    
    $newName = $null
    
    # Check if filename ends with _a, _b, _c, etc.
    if ($baseName -match '(.+)_([a-f])$') {
        $seriesPart = $matches[1]
        $suffix = $matches[2]
        
        # Extract just the number from series part (e.g., "86" from "Series_86")
        if ($seriesPart -match '(\d+)$') {
            $seriesNumber = $matches[1]
            
            # Map suffix to view type
            if ($suffix -eq 'a') {
                $newName = "series_${seriesNumber}_HEAD.png"
            }
            elseif ($suffix -eq 'b') {
                $newName = "series_${seriesNumber}_SILL.png"
            }
            elseif ($suffix -eq 'c') {
                $newName = "series_${seriesNumber}_JAMB.png"
            }
            elseif ($suffix -eq 'd' -or $suffix -eq 'e' -or $suffix -eq 'f') {
                Write-Host "Skipped (type $suffix): $originalName" -ForegroundColor Gray
                $skippedCount++
                continue
            }
        }
    }
    
    # If we couldn't parse the filename, skip it
    if (-not $newName) {
        Write-Host "Skipped (invalid format): $originalName" -ForegroundColor Gray
        $skippedCount++
        continue
    }
    
    # Build destination path
    $destFilePath = Join-Path $DestDir $newName
    
    # Check if destination file already exists
    if (Test-Path $destFilePath) {
        Write-Host "Already exists: $newName" -ForegroundColor Yellow
        continue
    }
    
    # Copy and rename the file
    try {
        Copy-Item -Path $file.FullName -Destination $destFilePath -Force
        Write-Host "Imported: $originalName -> $newName" -ForegroundColor Green
        $importedCount++
    }
    catch {
        Write-Host "Error importing $originalName : $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Import Summary" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Imported: $importedCount files" -ForegroundColor Green
Write-Host "Skipped: $skippedCount files" -ForegroundColor Yellow
Write-Host "Destination: $DestDir" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

if ($importedCount -gt 0) {
    Write-Host "SUCCESS! Frame images imported." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. In backend folder: uvicorn main:app --reload" -ForegroundColor White
    Write-Host "  2. Refresh browser at http://localhost:3000" -ForegroundColor White
}
else {
    Write-Host "No files imported. Check source folder and filename format." -ForegroundColor Yellow
}

Write-Host ""
