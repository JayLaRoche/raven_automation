#!/usr/bin/env pwsh
# Raven Shop Automation - File Cleanup Script
# Safely archives unnecessary files to archive folder

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveRoot = ".\archive_$timestamp"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "RAVEN SHOP AUTOMATION - FILE CLEANUP & ARCHIVE" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Archive location: $archiveRoot" -ForegroundColor Yellow
Write-Host ""

# Create archive directories
$directories = @(
    "$archiveRoot\old_cad_system",
    "$archiveRoot\pdf_layout_analyzer",
    "$archiveRoot\test_scripts",
    "$archiveRoot\generation_scripts",
    "$archiveRoot\documentation",
    "$archiveRoot\misc"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

Write-Host "[1] OLD CAD DRAWING SYSTEM" -ForegroundColor Green
Write-Host "--------------------------------------------------------------------------------"

$oldCadFiles = @(
    "app\services\cad_drawing_generator.py",
    "app\services\cad_data_transformer.py",
    "app\services\frame_profiles.py",
    "routers\cad_drawings.py",
    "services\drawing_generator.py"
)

$movedCount = 0
foreach ($file in $oldCadFiles) {
    if (Test-Path $file) {
        $destination = "$archiveRoot\old_cad_system\$(Split-Path $file -Leaf)"
        Move-Item $file $destination -Force
        Write-Host "  Archived: $file" -ForegroundColor Gray
        $movedCount++
    }
}
Write-Host "  Moved $movedCount files" -ForegroundColor Green
Write-Host ""

Write-Host "[2] PDF LAYOUT ANALYZER" -ForegroundColor Green
Write-Host "--------------------------------------------------------------------------------"

$layoutFiles = @(
    "app\services\pdf_layout_analyzer.py",
    "app\services\visual_template_generator.py",
    "analyze_layout.py"
)

$movedCount = 0
foreach ($file in $layoutFiles) {
    if (Test-Path $file) {
        $destination = "$archiveRoot\pdf_layout_analyzer\$(Split-Path $file -Leaf)"
        Move-Item $file $destination -Force
        Write-Host "  Archived: $file" -ForegroundColor Gray
        $movedCount++
    }
}
Write-Host "  Moved $movedCount files" -ForegroundColor Green
Write-Host ""

Write-Host "[3] TEST SCRIPTS" -ForegroundColor Green
Write-Host "--------------------------------------------------------------------------------"

$testFiles = @(
    "test_phase1.py",
    "test_cad_generator.py",
    "test_nail_flanges.py",
    "test_new_features.py",
    "test_layout_system.py",
    "test_complete_integration.py",
    "test_sheets_integration.py",
    "test_sheets_diagnostic.py",
    "test_drawing_generation.py",
    "verify_phase1.py",
    "validate_integration.py",
    "deployment_check.py"
)

$movedCount = 0
foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Move-Item $file "$archiveRoot\test_scripts\$file" -Force
        Write-Host "  Archived: $file" -ForegroundColor Gray
        $movedCount++
    }
}
Write-Host "  Moved $movedCount files" -ForegroundColor Green
Write-Host ""

Write-Host "[4] GENERATION SCRIPTS" -ForegroundColor Green
Write-Host "--------------------------------------------------------------------------------"

$genFiles = @(
    "phase1_quickstart.py",
    "quick_start.py",
    "generate_test1_pdf.py",
    "generate_test1_drawings.py",
    "generate_with_output.py",
    "generate_single_drawing.py",
    "generate_from_sheet.py",
    "generate_drawings_interactive.py",
    "generate_evergreen_drawings.py",
    "direct_generate.py",
    "run_test.py",
    "check_and_generate.py",
    "check_pdfs.py",
    "debug_test1.py",
    "status_report.py",
    "integration_test_demo.py",
    "full_test.py",
    "analyze_sheet_structure.py",
    "check_index_sheet.py",
    "list_sheets.py",
    "list_files.py"
)

$movedCount = 0
foreach ($file in $genFiles) {
    if (Test-Path $file) {
        Move-Item $file "$archiveRoot\generation_scripts\$file" -Force
        Write-Host "  Archived: $file" -ForegroundColor Gray
        $movedCount++
    }
}
Write-Host "  Moved $movedCount files" -ForegroundColor Green
Write-Host ""

Write-Host "[5] DOCUMENTATION FILES" -ForegroundColor Green
Write-Host "--------------------------------------------------------------------------------"

$docFiles = @(
    "PHASE1_README.md",
    "PHASE1_IMPLEMENTATION.py",
    "PHASE1_VISUAL_GUIDE.md",
    "PHASE1_DELIVERY.md",
    "README_CAD.md",
    "README_VISUAL.md",
    "README_INTEGRATION.md",
    "CAD_IMPLEMENTATION_SUMMARY.md",
    "CAD_DRAWING_GUIDE.md",
    "COMPLETION_SUMMARY.md",
    "INDEX.md",
    "INTEGRATION_GUIDE.md",
    "INTEGRATION_COMPLETE.md",
    "IMPLEMENTATION_SUMMARY.md",
    "DRAWING_UPDATE_SUMMARY.md",
    "LAYOUT_SYSTEM_COMPLETE.md",
    "DEPENDENCIES.md",
    "DEPLOYMENT_CHECKLIST.md",
    "DRAWING_API.md",
    "DRAWING_API_EXAMPLES.py"
)

$movedCount = 0
foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Move-Item $file "$archiveRoot\documentation\$file" -Force
        Write-Host "  Archived: $file" -ForegroundColor Gray
        $movedCount++
    }
}
Write-Host "  Moved $movedCount files" -ForegroundColor Green
Write-Host ""

Write-Host "[6] MISCELLANEOUS FILES" -ForegroundColor Green
Write-Host "--------------------------------------------------------------------------------"

$miscFiles = @(
    "config.py",
    "wrapper.py",
    "call_api.py",
    "post_generate.py",
    "get-pip.py",
    "create_batch_package.py",
    "deployment_checklist.py",
    "__init__.py"
)

$movedCount = 0
foreach ($file in $miscFiles) {
    if (Test-Path $file) {
        Move-Item $file "$archiveRoot\misc\$file" -Force
        Write-Host "  Archived: $file" -ForegroundColor Gray
        $movedCount++
    }
}
Write-Host "  Moved $movedCount files" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "CLEANUP COMPLETE" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Archive Location: $archiveRoot" -ForegroundColor Yellow
Write-Host ""
Write-Host "PRODUCTION FILES PRESERVED:" -ForegroundColor Green
Write-Host "  - main.py (FastAPI entry point)" -ForegroundColor White
Write-Host "  - app/models.py, app/database.py" -ForegroundColor White
Write-Host "  - routers/projects.py, routers/drawings.py" -ForegroundColor White
Write-Host "  - services/drawing_engine/ (all files)" -ForegroundColor White
Write-Host "  - app/services/reference_data_validator.py" -ForegroundColor White
Write-Host "  - backup_database.py, system_status.py" -ForegroundColor White
Write-Host ""
Write-Host "ARCHIVED CATEGORIES:" -ForegroundColor Yellow
Get-ChildItem $archiveRoot -Directory | ForEach-Object {
    $count = (Get-ChildItem $_.FullName -File).Count
    Write-Host "  - $($_.Name): $count files" -ForegroundColor Gray
}
Write-Host ""
Write-Host "To permanently delete:" -ForegroundColor Cyan
Write-Host "  Remove-Item -Recurse -Force $archiveRoot" -ForegroundColor White
Write-Host ""
