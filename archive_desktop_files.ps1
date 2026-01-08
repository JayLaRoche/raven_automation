# Archive Cleanup Script for Web App Migration
# Moves desktop app and unused files to archive

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archivePath = "archive_desktop_app_$timestamp"

Write-Host "=" * 60
Write-Host "Archiving Desktop Application Files"
Write-Host "=" * 60

# Create archive directory
New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
Write-Host "`nCreated archive: $archivePath"

# Files and folders to archive from multipleWindow3dScene
$itemsToArchive = @(
    "src",
    "database",
    "scripts",
    ".env",
    ".env.example",
    "requirements.txt",
    "README_DESKTOP.md",
    "IMPLEMENTATION_SUMMARY.md"
)

Write-Host "`nArchiving items:"
foreach ($item in $itemsToArchive) {
    $sourcePath = "C:\Users\larochej3\multipleWindow3dScene\$item"
    if (Test-Path $sourcePath) {
        $destPath = Join-Path $archivePath $item
        Move-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "  ✓ $item"
    }
}

Write-Host "`n" + "=" * 60
Write-Host "Archive Complete!"
Write-Host "=" * 60
Write-Host "`nArchived files moved to: $archivePath"
Write-Host "You can delete this archive later if not needed."
