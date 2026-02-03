# Raven Shop Automation - Project Cleanup Script
# Run this from the project root directory
# Purpose: Organize documentation and remove redundant files

Write-Host "🚀 Starting Raven Shop Automation Cleanup..." -ForegroundColor Cyan
Write-Host ""

# Ensure we're in the project root
if (-not (Test-Path "docker-compose.yml")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Create directory structure
Write-Host "📁 Creating organized folder structure..." -ForegroundColor Yellow
$folders = @(
    "docs",
    "docs/architecture",
    "docs/features",
    "docs/setup",
    "docs/api",
    "docs/database",
    "docs/archived",
    "scripts"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
        Write-Host "  ✓ Created: $folder" -ForegroundColor Green
    } else {
        Write-Host "  ○ Exists: $folder" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "📦 Moving files to organized structure..." -ForegroundColor Yellow

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination
    )
    
    if (Test-Path $Source) {
        try {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  ✓ Moved: $Source -> $Destination" -ForegroundColor Green
            return $true
        } catch {
            Write-Host "  ⚠ Warning: Could not move $Source - $_" -ForegroundColor Yellow
            return $false
        }
    } else {
        Write-Host "  ○ Not found: $Source" -ForegroundColor Gray
        return $false
    }
}

# ARCHITECTURE DOCS
Write-Host "`n📐 Architecture Documentation:" -ForegroundColor Cyan
Move-FileSafely "ARCHITECTURE_DIAGRAM.md" "docs/architecture/"
Move-FileSafely "APP_REORGANIZATION_INDEX.md" "docs/architecture/"
Move-FileSafely "DESIGN_SYSTEM_INDEX.md" "docs/architecture/"

# FEATURE DOCS
Write-Host "`n🎯 Feature Documentation:" -ForegroundColor Cyan
Move-FileSafely "FEATURE_IMPLEMENTATION_WINDOW_DOOR_SELECTOR.md" "docs/features/"
Move-FileSafely "DYNAMIC_SHEET_SELECTION.md" "docs/features/"
Move-FileSafely "FRAME_SERIES_DROPDOWN.md" "docs/features/"
Move-FileSafely "FRAME_SERIES_IMAGES.md" "docs/features/"
Move-FileSafely "CANVAS_HEADER_STICKY_INDEX.md" "docs/features/"
Move-FileSafely "DIAGNOSTIC_REPORT_GENERATOR_PAGE.md" "docs/features/"

# SETUP DOCS
Write-Host "`n⚙️ Setup Documentation:" -ForegroundColor Cyan
Move-FileSafely "GETTING_STARTED.md" "docs/setup/"
Move-FileSafely "ENVIRONMENT_SETUP.md" "docs/setup/"
Move-FileSafely "ENVIRONMENT_DOCUMENTATION_INDEX.md" "docs/setup/"
Move-FileSafely "DEPLOYMENT_CHECKLIST.md" "docs/setup/"
Move-FileSafely "CLICK_TO_RUN.md" "docs/setup/"
Move-FileSafely "CANVAS_SETUP_GUIDE.md" "docs/setup/"

# API DOCS
Write-Host "`n🔌 API Documentation:" -ForegroundColor Cyan
Move-FileSafely "API_DOCUMENTATION.md" "docs/api/"
Move-FileSafely "HOW_TO_GENERATE_DRAWING.md" "docs/api/"
Move-FileSafely "CODE_EXAMPLES_AND_USAGE_GUIDE.md" "docs/api/"

# DATABASE DOCS
Write-Host "`n🗄️ Database Documentation:" -ForegroundColor Cyan
Move-FileSafely "FRAME_DATABASE_CONNECTION.md" "docs/database/"
Move-FileSafely "FRAME_DATABASE_QUICKSTART.md" "docs/database/"
Move-FileSafely "FRAME_MIGRATION_QUICK_REF.md" "docs/database/"
Move-FileSafely "GOOGLE_SHEETS_STATUS.md" "docs/database/"

# ROOT REFERENCE DOCS (Keep these accessible)
Write-Host "`n📚 Root Reference Documentation:" -ForegroundColor Cyan
Move-FileSafely "IMPLEMENTATION_INDEX.md" "docs/"
Move-FileSafely "IMPLEMENTATION_STATUS.md" "docs/"
Move-FileSafely "FILE_INDEX.md" "docs/"
Move-FileSafely "GIT_COMMIT_GUIDE.md" "docs/"

# SCRIPTS
Write-Host "`n🔧 Utility Scripts:" -ForegroundColor Cyan
Move-FileSafely "archive_desktop_files.ps1" "scripts/"
Move-FileSafely "import_frames.ps1" "scripts/"
Move-FileSafely "debug_pdf.py" "scripts/"

# ARCHIVE REDUNDANT DOCS
Write-Host "`n🗑️ Archiving Redundant Documentation:" -ForegroundColor Cyan
$redundantFiles = @(
    # App Reorganization duplicates
    "APP_REORGANIZATION_COMPLETE.md",
    "APP_REORGANIZATION_COMPLETION.md",
    "APP_REORGANIZATION_QUICK_REF.md",
    "APP_REORGANIZATION_SUMMARY.md",
    "APP_REORGANIZATION_VISUAL_ARCHITECTURE.md",
    
    # Canvas Sticky duplicates
    "CANVAS_HEADER_STICKY_BEFORE_AFTER.md",
    "CANVAS_HEADER_STICKY_FIX.md",
    "CANVAS_HEADER_STICKY_QUICK_REF.md",
    "CANVAS_HEADER_STICKY_SUMMARY.md",
    "CANVAS_HEADER_STICKY_VISUAL_TEST.md",
    
    # Design System duplicates
    "DESIGN_IMPLEMENTATION_GUIDE.md",
    "DESIGN_SYSTEM_COMPLETE.md",
    "DESIGN_SYSTEM_DELIVERABLES.md",
    "DESIGN_TOKENS_EXTRACTED.md",
    "DESIGN_QUICK_REFERENCE.txt",
    
    # Frame Migration duplicates
    "FRAME_MIGRATION_COMPLETE.md",
    "FRAME_MIGRATION_TASKS_COMPLETE.md",
    "FRAME_SYNC_IMPLEMENTATION.md",
    
    # Frame Images duplicates
    "FRAME_IMAGES_FIX_COMPLETE.md",
    "FRAME_IMAGES_INTEGRATION_TEST.md",
    "FRAME_IMAGES_UPDATE.md",
    "FRAME_IMAGES_REFERENCE.md",
    "FRAME_IMAGES_QUICK_REFERENCE.md",
    
    # Implementation duplicates
    "IMPLEMENTATION_CODE_DETAILS.md",
    "IMPLEMENTATION_COMPLETE.md",
    "IMPLEMENTATION_COMPLETE.txt",
    "IMPLEMENTATION_SUMMARY.md",
    "IMPLEMENTATION_VERIFICATION_v2.md",
    "IMPLEMENTATION_CHECKLIST.md",
    
    # Environment duplicates
    "ENVIRONMENT_AUDIT_COMPLETE.md",
    "ENVIRONMENT_CONFIGURATION_SUMMARY.md",
    "ENV_QUICK_REFERENCE.md",
    
    # Completion/Fix files
    "COMPLETION_STATUS.txt",
    "COMPLETION_STATUS_WINDOW_DOOR_FEATURE.md",
    "FIX_SUMMARY.txt",
    "FIX_DRAWINGS_ENDPOINT_404.md",
    "GENERATOR_PAGE_FIX_SUMMARY.md",
    "FAILED_DRAWING_GENERATION_DEBUG.md",
    
    # Other redundant
    "CHANGES_SUMMARY.md",
    "CODE_CHANGES_REFERENCE.md"
)

$movedCount = 0
foreach ($file in $redundantFiles) {
    if (Move-FileSafely $file "docs/archived/") {
        $movedCount++
    }
}

Write-Host ""
Write-Host "📊 Cleanup Summary:" -ForegroundColor Cyan
Write-Host "  • Files archived: $movedCount" -ForegroundColor White
Write-Host "  • New structure created in: docs/" -ForegroundColor White
Write-Host "  • Scripts moved to: scripts/" -ForegroundColor White

Write-Host ""
Write-Host "⚠️ NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Review archived files in: docs/archived/" -ForegroundColor White
Write-Host "  2. If everything looks good, run:" -ForegroundColor White
Write-Host "     Remove-Item 'docs/archived' -Recurse -Force" -ForegroundColor Gray
Write-Host "  3. Commit changes to Git" -ForegroundColor White
Write-Host ""

# Generate report
$reportPath = "docs/CLEANUP_REPORT.md"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$reportContent = @"
# Project Cleanup Report
Generated: $timestamp

## Summary
- **Files Archived**: $movedCount
- **New Folder Structure**: Created organized docs/ and scripts/ directories
- **Status**: ✅ Cleanup Complete

## New Structure
docs/
├── architecture/       # System design & reorganization docs
├── features/          # Feature-specific documentation
├── setup/             # Getting started & environment setup
├── api/               # API documentation & examples
├── database/          # Database & migration docs
├── archived/          # Redundant files (review before deleting)
├── IMPLEMENTATION_INDEX.md
├── IMPLEMENTATION_STATUS.md
├── FILE_INDEX.md
└── GIT_COMMIT_GUIDE.md

scripts/               # Utility scripts
├── archive_desktop_files.ps1
├── import_frames.ps1
└── debug_pdf.py

## Archived Files
Review these files in docs/archived/ before permanent deletion:
$($redundantFiles | ForEach-Object { "- $_" } | Out-String)

## Recommended Actions
1. ✅ Review archived files
2. ✅ Test application functionality
3. ✅ Delete archived folder if satisfied
4. ✅ Commit organized structure to Git

## Notes
- Original INDEX.md kept at root for quick reference
- .env and .env.example preserved
- docker-compose.yml remains at root
- All critical documentation retained and organized
"@

Set-Content -Path $reportPath -Value $reportContent
Write-Host "📄 Cleanup report generated: $reportPath" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Cleanup Complete!" -ForegroundColor Green