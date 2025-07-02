# Bulk Upload Wan2GP Implementation to GitHub
# PowerShell script to upload all Wan2GP files to the WanBook repository

param(
    [string]$GitHubToken = $env:GITHUB_TOKEN,
    [string]$Owner = "remphanstar",
    [string]$Repo = "WanBook",
    [string]$SourcePath = "C:\Users\Greepo\Documents\Cline\Workflows\Porxo\WanBook-1\Wan2GP"
)

Write-Host "WanBook Wan2GP Bulk Upload Script" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if source directory exists
if (!(Test-Path $SourcePath)) {
    Write-Host "Error: Source directory not found: $SourcePath" -ForegroundColor Red
    exit 1
}

# Check GitHub token
if (!$GitHubToken) {
    Write-Host "Error: GitHub token not provided. Set GITHUB_TOKEN environment variable or pass as parameter." -ForegroundColor Red
    exit 1
}

# Function to upload file to GitHub
function Upload-FileToGitHub {
    param(
        [string]$FilePath,
        [string]$GitHubPath,
        [string]$Content,
        [string]$Message
    )
    
    $headers = @{
        "Authorization" = "token $GitHubToken"
        "Accept" = "application/vnd.github.v3+json"
    }
    
    $body = @{
        message = $Message
        content = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Content))
    } | ConvertTo-Json
    
    $uri = "https://api.github.com/repos/$Owner/$Repo/contents/$GitHubPath"
    
    try {
        $response = Invoke-RestMethod -Uri $uri -Method PUT -Headers $headers -Body $body
        Write-Host "✅ Uploaded: $GitHubPath" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to upload $GitHubPath`: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to check if file should be uploaded (skip large binary files)
function Should-UploadFile {
    param([string]$FilePath)
    
    $extension = [System.IO.Path]::GetExtension($FilePath).ToLower()
    $fileName = [System.IO.Path]::GetFileName($FilePath)
    
    # Skip large binary files that should use Git LFS
    $skipExtensions = @('.bin', '.pt', '.pth', '.safetensors', '.ckpt', '.pkl', '.h5', '.mp4', '.avi', '.mov', '.zip', '.tar.gz')
    
    if ($skipExtensions -contains $extension) {
        Write-Host "⏭️ Skipping large file (use Git LFS): $fileName" -ForegroundColor Yellow
        return $false
    }
    
    # Skip very large files (>50MB)
    $fileInfo = Get-Item $FilePath
    if ($fileInfo.Length -gt 50MB) {
        Write-Host "⏭️ Skipping large file (>50MB): $fileName" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

# Get all files recursively
Write-Host "Scanning directory: $SourcePath" -ForegroundColor Cyan
$allFiles = Get-ChildItem -Path $SourcePath -Recurse -File

$totalFiles = $allFiles.Count
$uploadedCount = 0
$skippedCount = 0
$failedCount = 0

Write-Host "Found $totalFiles files to process" -ForegroundColor Cyan
Write-Host ""

foreach ($file in $allFiles) {
    $relativePath = $file.FullName.Substring($SourcePath.Length + 1).Replace('\', '/')
    $gitHubPath = "Wan2GP/$relativePath"
    
    Write-Host "Processing: $relativePath" -ForegroundColor White
    
    if (Should-UploadFile $file.FullName) {
        try {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
            $message = "Add Wan2GP implementation file: $relativePath"
            
            if (Upload-FileToGitHub -FilePath $file.FullName -GitHubPath $gitHubPath -Content $content -Message $message) {
                $uploadedCount++
            } else {
                $failedCount++
            }
        }
        catch {
            Write-Host "❌ Error reading file $($file.FullName): $($_.Exception.Message)" -ForegroundColor Red
            $failedCount++
        }
    } else {
        $skippedCount++
    }
    
    # Brief pause to avoid rate limiting
    Start-Sleep -Milliseconds 100
}

Write-Host ""
Write-Host "Upload Summary:" -ForegroundColor Green
Write-Host "  Total files: $totalFiles"
Write-Host "  Uploaded: $uploadedCount" -ForegroundColor Green
Write-Host "  Skipped: $skippedCount" -ForegroundColor Yellow
Write-Host "  Failed: $failedCount" -ForegroundColor $(if ($failedCount -eq 0) { "Green" } else { "Red" })

if ($failedCount -eq 0) {
    Write-Host ""
    Write-Host "✅ Wan2GP implementation successfully uploaded to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/$Owner/$Repo" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️ Upload completed with some failures. Check the output above for details." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Large files (skipped) should be added with Git LFS if needed"
Write-Host "2. Test the OpusWan(1).ipynb notebook with the complete repository"
Write-Host "3. Update documentation to reflect the complete structure"