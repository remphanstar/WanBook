# Fix for Cell 4 - Repository Management

The error shows that the `action` variable is not properly defined before being used. Here's the corrected version:

```python
# ================================================================================
# 📦 REPOSITORY MANAGEMENT - FIXED VERSION
# ================================================================================

import os
import subprocess
import sys
from pathlib import Path

def clone_or_update_repo():
    """Clone or update the WanBook repository with proper error handling."""
    
    # Configuration
    repo_name = "WanBook"
    repo_url = "https://github.com/remphanstar/WanBook.git"
    repo_path = Path(f"/content/{repo_name}")
    
    # Initialize action variable properly
    action = "clone"  # Default action
    
    try:
        # Determine action based on repository state
        if repo_path.exists() and (repo_path / ".git").exists():
            action = "update"
            print(f"[INFO] Repository exists, will update...")
        else:
            action = "clone"
            print(f"[INFO] Repository not found, will clone...")
        
        # Execute based on action
        if action == "update":
            print(f"[1/3] Updating existing repository...")
            os.chdir(repo_path)
            
            # Fetch latest changes
            result = subprocess.run(
                ["git", "fetch", "origin"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"⚠️ Fetch warning: {result.stderr}")
            
            # Pull latest changes
            result = subprocess.run(
                ["git", "pull", "origin", "main"], 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Repository updated successfully!")
            else:
                print(f"⚠️ Update had issues: {result.stderr}")
                print("📌 Continuing with existing repository...")
        
        elif action == "clone":
            print(f"[1/3] Cloning repository from GitHub...")
            
            # Remove existing directory if it exists but isn't a git repo
            if repo_path.exists():
                import shutil
                shutil.rmtree(repo_path)
            
            # Clone the repository
            result = subprocess.run(
                ["git", "clone", repo_url, str(repo_path)], 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            
            if result.returncode == 0:
                print("✅ Repository cloned successfully!")
            else:
                raise Exception(f"Git clone failed: {result.stderr}")
        
        # Verify repository structure
        print(f"[2/3] Verifying repository structure...")
        
        # Check for key files
        key_files = [
            "OpusWan(1).ipynb",
            "requirements.txt", 
            "Wan2GP",
            "README.md"
        ]
        
        missing_files = []
        for file_name in key_files:
            file_path = repo_path / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            print(f"⚠️ Some files missing: {missing_files}")
            print("📌 Repository may be incomplete, but continuing...")
        else:
            print("✅ All key files found!")
        
        # Set working directory
        print(f"[3/3] Setting up working directory...")
        os.chdir(repo_path)
        print(f"✅ Working directory: {os.getcwd()}")
        
        # Display repository info
        print("\n" + "="*60)
        print("📊 REPOSITORY STATUS")
        print("="*60)
        print(f"📂 Location: {repo_path}")
        print(f"🔧 Action taken: {action}")
        print(f"📁 Contents: {len(list(repo_path.iterdir()))} items")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Git operation timed out. Check your internet connection.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Repository setup failed: {e}")
        return False

# Execute repository setup with comprehensive error handling
print("="*80)
print("📦 REPOSITORY MANAGEMENT")
print("="*80)

try:
    success = clone_or_update_repo()
    if not success:
        print("\n🔧 Manual steps if automatic setup fails:")
        print("1. Check internet connection")
        print("2. Try: !git clone https://github.com/remphanstar/WanBook.git")
        print("3. Or download ZIP manually from GitHub")
        print("4. Restart this cell after manual setup")
except Exception as e:
    print(f"❌ Critical error: {e}")
    print("\n🆘 Fallback options:")
    print("1. Restart runtime and try again")
    print("2. Use !git clone command manually") 
    print("3. Download repository as ZIP file")
```

## Key Fixes Applied:

1. **Variable Initialization**: Added `action = "clone"` as default before conditional logic
2. **Proper Error Handling**: Comprehensive try/catch blocks with specific error types
3. **Timeout Protection**: Added timeouts to prevent hanging operations
4. **Validation Steps**: Check for key files and repository structure
5. **Fallback Instructions**: Clear manual steps if automation fails
6. **Better Logging**: More detailed progress and status information

This should resolve the `UnboundLocalError` and provide better reliability for the repository management cell.