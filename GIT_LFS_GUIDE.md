# Git LFS Requirements for WanBook Repository

## Files That NEED Git LFS

The following file types in the Wan2GP directory structure require Git LFS due to size constraints:

### 🤖 Model Files (Critical - Usually 100MB+)
```
**Required Git LFS extensions already configured:**
- *.bin (PyTorch models, tokenizers)
- *.pt / *.pth (PyTorch weights)
- *.safetensors (SafeTensors format)
- *.ckpt (Checkpoint files)
- *.pkl (Pickle files with model weights)
- *.h5 (HDF5 model files)
```

### 📁 Directories Likely to Contain Large Files

#### LoRA Directories
- `Wan2GP/loras_hunyuan/` - HunyuanVideo LoRA weights
- `Wan2GP/loras_hunyuan_i2v/` - HunyuanVideo I2V LoRA weights  
- `Wan2GP/loras_ltxv/` - LTX-Video LoRA weights
- **Typical files**: `*.safetensors`, `*.bin`, `*.pt`

#### Preprocessing Models
- `Wan2GP/preprocessing/dwpose/` - DWPose model weights
- `Wan2GP/preprocessing/matanyone/` - MATAnyone model weights
- `Wan2GP/preprocessing/midas/` - MiDaS depth estimation weights
- **Typical files**: `*.pth`, `*.pt`, `*.onnx`

#### Assets Directory
- `Wan2GP/assets/` - Example videos, reference images
- **Typical files**: `*.mp4`, `*.png`, `*.jpg` (if high-resolution)

#### Model Configurations with Weights
- `Wan2GP/hyvideo/` - May contain cached model files
- `Wan2GP/ltx_video/` - May contain cached model files
- `Wan2GP/wan/` - May contain cached model files

### 🎥 Media Files (Already Configured)
```
- *.mp4, *.avi, *.mov, *.mkv, *.webm (videos)
- *.tiff, *.tif (large images)
```

### 📦 Archive Files (Already Configured)
```
- *.zip, *.tar.gz, *.tar.bz2, *.7z
```

## Current Git LFS Configuration Status

✅ **Already configured** in `.gitattributes`:
```gitattributes
# Large model files
*.bin filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
*.safetensors filter=lfs diff=lfs merge=lfs -text
*.ckpt filter=lfs diff=lfs merge=lfs -text
*.pkl filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text

# Video files
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.avi filter=lfs diff=lfs merge=lfs -text
*.mov filter=lfs diff=lfs merge=lfs -text
*.mkv filter=lfs diff=lfs merge=lfs -text
*.webm filter=lfs diff=lfs merge=lfs -text

# Large image files
*.tiff filter=lfs diff=lfs merge=lfs -text
*.tif filter=lfs diff=lfs merge=lfs -text

# Archive files
*.zip filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
*.tar.bz2 filter=lfs diff=lfs merge=lfs -text
*.7z filter=lfs diff=lfs merge=lfs -text
```

## Upload Strategy

### For Regular Upload Script
The `upload_wan2gp.ps1` script will:
- ✅ **Upload small files** (Python code, configs, docs)
- ⏭️ **Skip large files** that need Git LFS
- 📝 **Report which files were skipped**

### For Large Files (Post-Upload)
After running the regular upload script, you'll need to:

1. **Initialize Git LFS** (if not already done):
```bash
git lfs install
```

2. **Add large files manually**:
```bash
git add Wan2GP/loras_hunyuan/*.safetensors
git add Wan2GP/preprocessing/dwpose/*.pth
git add Wan2GP/assets/*.mp4
# etc.
```

3. **Commit and push**:
```bash
git commit -m "Add large model files via Git LFS"
git push
```

## Recommended Approach

1. **First**: Run the `upload_wan2gp.ps1` script to upload all small files
2. **Then**: Check what large files were skipped
3. **Finally**: Use Git LFS to add the large files

## Files That DON'T Need Git LFS

✅ **Safe for regular upload**:
- `*.py` (Python source code)
- `*.yaml`, `*.yml` (Configuration files)
- `*.json` (JSON configs)
- `*.md`, `*.txt` (Documentation)
- `requirements.txt`
- Small `*.png`, `*.jpg` images (<25MB)

---

**Important**: The repository is already configured for Git LFS, so when you do have large files to add, they'll be handled automatically based on the extensions.