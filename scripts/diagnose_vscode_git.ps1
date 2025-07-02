# VS Code Git Configuration Diagnostic and Fix Script
# Run this script in PowerShell to diagnose and fix VS Code/Git user issues

Write-Host "=== VS Code Git Configuration Diagnostic ===" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
$projectPath = "c:\Users\Greepo\Documents\Cline\Workflows\Porxo\WanBook-1"
if (Test-Path $projectPath) {
    Set-Location $projectPath
    Write-Host "✓ Navigated to project directory: $projectPath" -ForegroundColor Green
} else {
    Write-Host "✗ Project directory not found: $projectPath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Current Git Configuration ===" -ForegroundColor Yellow

# Check Git version
Write-Host "Git Version:" -ForegroundColor Cyan
git --version

Write-Host ""
Write-Host "Global Git Settings:" -ForegroundColor Cyan
Write-Host "Name: $(git config --global user.name)"
Write-Host "Email: $(git config --global user.email)"

Write-Host ""
Write-Host "Local Git Settings:" -ForegroundColor Cyan
Write-Host "Name: $(git config --local user.name)"
Write-Host "Email: $(git config --local user.email)"

Write-Host ""
Write-Host "Remote Repository:" -ForegroundColor Cyan
git remote -v

Write-Host ""
Write-Host "Current Branch Status:" -ForegroundColor Cyan
git branch -vv

Write-Host ""
Write-Host "Recent Commits:" -ForegroundColor Cyan
git log --oneline -5

Write-Host ""
Write-Host "=== Credential Manager Check ===" -ForegroundColor Yellow
$gitCredential = cmdkey /list | Select-String "git:https://github.com"
if ($gitCredential) {
    Write-Host "✓ GitHub credential found in Windows Credential Manager" -ForegroundColor Green
    Write-Host $gitCredential
} else {
    Write-Host "✗ No GitHub credential found in Windows Credential Manager" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== VS Code Settings Check ===" -ForegroundColor Yellow
$vscodeSettingsPath = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $vscodeSettingsPath) {
    Write-Host "✓ VS Code settings file exists: $vscodeSettingsPath" -ForegroundColor Green
    Write-Host "Git-related settings:" -ForegroundColor Cyan
    Get-Content $vscodeSettingsPath | Select-String "git" -Context 1
} else {
    Write-Host "✗ VS Code settings file not found: $vscodeSettingsPath" -ForegroundColor Red
    Write-Host "Creating basic VS Code settings file..." -ForegroundColor Yellow
    
    $settingsDir = Split-Path -Parent $vscodeSettingsPath
    if (-not (Test-Path $settingsDir)) {
        New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
    }
    
    $basicSettings = @'
{
    "git.defaultCloneDirectory": "c:\\Users\\Greepo\\Documents\\GitHub",
    "git.autofetch": true,
    "git.confirmSync": false,
    "git.enableSmartCommit": true,
    "git.enableStatusBarSync": true,
    "terminal.integrated.defaultProfile.windows": "PowerShell"
}
'@
    
    $basicSettings | Out-File -FilePath $vscodeSettingsPath -Encoding UTF8
    Write-Host "✓ Created basic VS Code settings file" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Configuration Fix Options ===" -ForegroundColor Yellow
Write-Host "1. Fix Global Git User Settings" -ForegroundColor Cyan
Write-Host "2. Fix Local Git User Settings" -ForegroundColor Cyan
Write-Host "3. Reset Git Credentials" -ForegroundColor Cyan
Write-Host "4. Clear VS Code Workspace Cache" -ForegroundColor Cyan
Write-Host "5. All of the above" -ForegroundColor Cyan
Write-Host "6. Skip fixes" -ForegroundColor Cyan

$choice = Read-Host "Enter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host "Setting global Git user..." -ForegroundColor Yellow
        git config --global user.name "remphanstar"
        git config --global user.email "zopiclone66@gmail.com"
        Write-Host "✓ Global Git user set to remphanstar" -ForegroundColor Green
    }
    "2" {
        Write-Host "Setting local Git user..." -ForegroundColor Yellow
        git config --local user.name "remphanstar"
        git config --local user.email "zopiclone66@gmail.com"
        Write-Host "✓ Local Git user set to remphanstar" -ForegroundColor Green
    }
    "3" {
        Write-Host "Resetting Git credentials..." -ForegroundColor Yellow
        git config --global --unset credential.helper
        git config --global credential.helper manager-core
        cmdkey /delete:git:https://github.com
        Write-Host "✓ Git credentials reset. You'll be prompted for credentials on next push/pull" -ForegroundColor Green
    }
    "4" {
        Write-Host "Clearing VS Code workspace cache..." -ForegroundColor Yellow
        $workspaceStoragePath = "$env:APPDATA\Code\User\workspaceStorage"
        if (Test-Path $workspaceStoragePath) {
            Remove-Item -Path $workspaceStoragePath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "✓ VS Code workspace cache cleared" -ForegroundColor Green
        } else {
            Write-Host "✓ VS Code workspace cache directory doesn't exist" -ForegroundColor Green
        }
    }
    "5" {
        Write-Host "Applying all fixes..." -ForegroundColor Yellow
        
        # Fix global Git user
        git config --global user.name "remphanstar"
        git config --global user.email "zopiclone66@gmail.com"
        Write-Host "✓ Global Git user set" -ForegroundColor Green
        
        # Fix local Git user
        git config --local user.name "remphanstar"
        git config --local user.email "zopiclone66@gmail.com"
        Write-Host "✓ Local Git user set" -ForegroundColor Green
        
        # Reset credentials
        git config --global --unset credential.helper
        git config --global credential.helper manager-core
        Write-Host "✓ Git credentials helper reset" -ForegroundColor Green
        
        # Clear VS Code cache
        $workspaceStoragePath = "$env:APPDATA\Code\User\workspaceStorage"
        if (Test-Path $workspaceStoragePath) {
            Remove-Item -Path $workspaceStoragePath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "✓ VS Code workspace cache cleared" -ForegroundColor Green
        }
        
        Write-Host "✓ All fixes applied!" -ForegroundColor Green
    }
    "6" {
        Write-Host "Skipping fixes..." -ForegroundColor Yellow
    }
    default {
        Write-Host "Invalid choice. Skipping fixes..." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Final Verification ===" -ForegroundColor Yellow
Write-Host "After fixes, your configuration should show:" -ForegroundColor Cyan
Write-Host "Global Name: $(git config --global user.name)"
Write-Host "Global Email: $(git config --global user.email)"
Write-Host "Local Name: $(git config --local user.name)"
Write-Host "Local Email: $(git config --local user.email)"

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Yellow
Write-Host "1. Close VS Code completely" -ForegroundColor Cyan
Write-Host "2. Reopen VS Code in this project directory" -ForegroundColor Cyan
Write-Host "3. Check the Source Control panel for correct user (remphanstar)" -ForegroundColor Cyan
Write-Host "4. Make a test commit to verify integration" -ForegroundColor Cyan
Write-Host "5. Delete the test_integration.md file from your repository" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== Diagnostic Complete ===" -ForegroundColor Green
Write-Host "If issues persist, check the GitHub credential in Windows Credential Manager:" -ForegroundColor Cyan
Write-Host "Control Panel > Credential Manager > Windows Credentials > git:https://github.com"