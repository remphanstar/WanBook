# Quick Fix Script for Username Issues
# This script fixes all remaining "remphanostar" references

Write-Host "=== Fixing Username Issues ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
$projectPath = "c:\Users\Greepo\Documents\Cline\Workflows\Porxo\WanBook-1"
if (Test-Path $projectPath) {
    Set-Location $projectPath
    Write-Host "✓ In project directory: $projectPath" -ForegroundColor Green
} else {
    Write-Host "✗ Project directory not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Current remote URL:" -ForegroundColor Yellow
git remote -v

Write-Host ""
Write-Host "=== FIXING REMOTE URL ===" -ForegroundColor Cyan
Write-Host "Updating remote URL from remphanostar to remphanstar..." -ForegroundColor Yellow

# Fix the remote URL
git remote set-url origin https://github.com/remphanstar/WanBook.git

Write-Host "✓ Remote URL updated!" -ForegroundColor Green
Write-Host ""
Write-Host "New remote URL:" -ForegroundColor Yellow
git remote -v

Write-Host ""
Write-Host "=== TESTING CONNECTION ===" -ForegroundColor Cyan
Write-Host "Testing connection to GitHub..." -ForegroundColor Yellow

# Test the connection
$testResult = git ls-remote --heads origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Successfully connected to remphanstar/WanBook!" -ForegroundColor Green
} else {
    Write-Host "✗ Connection failed. You may need to update credentials." -ForegroundColor Red
    Write-Host "Error: $testResult" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== UPDATING CREDENTIALS ===" -ForegroundColor Cyan
Write-Host "Clearing old credentials and setting up fresh ones..." -ForegroundColor Yellow

# Remove old credential
cmdkey /delete:git:https://github.com 2>$null

# Set up credential helper
git config --global credential.helper manager-core

Write-Host "✓ Credentials cleared. You'll be prompted for new credentials on next push/pull." -ForegroundColor Green

Write-Host ""
Write-Host "=== VS CODE SETTINGS ===" -ForegroundColor Cyan
$vscodeSettings = "$env:APPDATA\Code\User\settings.json"

if (Test-Path $vscodeSettings) {
    Write-Host "✓ VS Code settings file exists" -ForegroundColor Green
    
    # Read current settings
    $settings = Get-Content $vscodeSettings -Raw | ConvertFrom-Json
    
    # Ensure Git settings are correct
    if (-not $settings.PSObject.Properties['git.defaultCloneDirectory']) {
        $settings | Add-Member -NotePropertyName 'git.defaultCloneDirectory' -NotePropertyValue 'c:\\Users\\Greepo\\Documents\\GitHub'
    }
    if (-not $settings.PSObject.Properties['git.autofetch']) {
        $settings | Add-Member -NotePropertyName 'git.autofetch' -NotePropertyValue $true
    }
    if (-not $settings.PSObject.Properties['git.enableSmartCommit']) {
        $settings | Add-Member -NotePropertyName 'git.enableSmartCommit' -NotePropertyValue $true
    }
    
    # Save updated settings
    $settings | ConvertTo-Json -Depth 10 | Out-File $vscodeSettings -Encoding UTF8
    Write-Host "✓ VS Code settings updated" -ForegroundColor Green
} else {
    Write-Host "Creating VS Code settings file..." -ForegroundColor Yellow
    $newSettings = @{
        'git.defaultCloneDirectory' = 'c:\\Users\\Greepo\\Documents\\GitHub'
        'git.autofetch' = $true
        'git.enableSmartCommit' = $true
        'git.enableStatusBarSync' = $true
        'terminal.integrated.defaultProfile.windows' = 'PowerShell'
    }
    
    $settingsDir = Split-Path $vscodeSettings
    if (-not (Test-Path $settingsDir)) {
        New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
    }
    
    $newSettings | ConvertTo-Json -Depth 10 | Out-File $vscodeSettings -Encoding UTF8
    Write-Host "✓ VS Code settings created" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== FINAL VERIFICATION ===" -ForegroundColor Cyan
Write-Host "Git User: $(git config user.name)" -ForegroundColor Yellow
Write-Host "Git Email: $(git config user.email)" -ForegroundColor Yellow
Write-Host "Remote URL: $(git remote get-url origin)" -ForegroundColor Yellow

Write-Host ""
Write-Host "=== NEXT STEPS ===" -ForegroundColor Green
Write-Host "1. Close VS Code completely" -ForegroundColor Cyan
Write-Host "2. Reopen VS Code in your project" -ForegroundColor Cyan
Write-Host "3. VS Code should now show 'remphanstar' as the user" -ForegroundColor Cyan
Write-Host "4. Make a test commit to verify everything works" -ForegroundColor Cyan

Write-Host ""
Write-Host "✅ All fixes applied! VS Code should now show the correct username." -ForegroundColor Green