# WanBook Workspace Cleanup Script
# This PowerShell script removes unnecessary files and folders from the local workspace

Write-Host "WanBook Workspace Cleanup Script" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

# Define the workspace root (adjust path as needed)
$workspaceRoot = "C:\Users\Greepo\Documents\Cline\Workflows\Porxo\WanBook-1"

Write-Host "Workspace root: $workspaceRoot" -ForegroundColor Yellow

# Check if workspace exists
if (!(Test-Path $workspaceRoot)) {
    Write-Host "Workspace directory not found: $workspaceRoot" -ForegroundColor Red
    exit 1
}

# Set location to workspace
Set-Location $workspaceRoot

# Files and folders to keep (whitelist approach)
$keepItems = @(
    "OpusWan(1).ipynb",
    "requirements.txt", 
    "README.md",
    "README_CLOUD_SETUP.md",
    "PROJECT_CONTEXT.md",
    "CHANGELOG.md",
    ".gitattributes",
    ".git",
    ".github"
)

# Files and folders to remove (based on analysis)
$removeItems = @(
    "cloud_launcher.py",
    "docker-compose.yml", 
    "Dockerfile",
    "launch_wan2gp.sh",
    "launch_wgp_setup.sh",
    "README_COMPLETE.md",
    "requirements_cloud.txt",
    "runpod_template.yaml",
    "setup_cloud.sh", 
    "vast_ai_template.json",
    "wan2gp_cloud_setup.ipynb",
    "WanGP_Launcher.ipynb",
    "src",
    "Wan2GP"
)

Write-Host "`nFiles and folders to remove:" -ForegroundColor Cyan
foreach ($item in $removeItems) {
    if (Test-Path $item) {
        Write-Host "  - $item (EXISTS)" -ForegroundColor Yellow
    } else {
        Write-Host "  - $item (NOT FOUND)" -ForegroundColor Gray
    }
}

Write-Host "`nDo you want to proceed with the cleanup? (y/N)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "`nStarting cleanup..." -ForegroundColor Green
    
    $removedCount = 0
    $errorCount = 0
    
    foreach ($item in $removeItems) {
        if (Test-Path $item) {
            try {
                if (Test-Path $item -PathType Container) {
                    Write-Host "Removing directory: $item" -ForegroundColor Yellow
                    Remove-Item $item -Recurse -Force
                } else {
                    Write-Host "Removing file: $item" -ForegroundColor Yellow
                    Remove-Item $item -Force
                }
                $removedCount++
                Write-Host "  ✓ Removed successfully" -ForegroundColor Green
            }
            catch {
                Write-Host "  ✗ Error removing $item`: $_" -ForegroundColor Red
                $errorCount++
            }
        }
    }
    
    Write-Host "`nCleanup Summary:" -ForegroundColor Green
    Write-Host "  Items removed: $removedCount" -ForegroundColor Green
    Write-Host "  Errors: $errorCount" -ForegroundColor $(if ($errorCount -eq 0) { "Green" } else { "Red" })
    
    Write-Host "`nRemaining files in workspace:" -ForegroundColor Cyan
    Get-ChildItem -Name | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor White
    }
    
    Write-Host "`nCleanup completed!" -ForegroundColor Green
    Write-Host "The workspace now contains only the files needed for OpusWan(1).ipynb" -ForegroundColor Green
    
} else {
    Write-Host "`nCleanup cancelled." -ForegroundColor Yellow
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Verify OpusWan(1).ipynb works correctly in the cleaned workspace" -ForegroundColor White
Write-Host "2. Test the notebook on a cloud GPU platform" -ForegroundColor White
Write-Host "3. All files are already uploaded to: https://github.com/remphanstar/WanBook" -ForegroundColor White

Write-Host "`nScript completed." -ForegroundColor Green