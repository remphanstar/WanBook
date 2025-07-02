# WanGP Cloud GPU Setup Guide

This repository contains everything needed to run WanGP (Wan Video Generation Platform) on any cloud GPU service.

## 🚀 Quick Start

### Option 1: Jupyter Notebook (Recommended)
Upload `OpusWan(1).ipynb` to your cloud platform and run all cells.

### Option 2: Manual Setup
```bash
git clone https://github.com/remphanstar/WanBook.git
cd WanBook
pip install -r requirements.txt
python wgp.py --share
```

## 🌐 Supported Cloud Platforms

- **Google Colab** - Free GPU access
- **Kaggle Notebooks** - Free GPU with time limits
- **RunPod** - Affordable cloud GPU rental
- **Vast.ai** - Community cloud GPU marketplace
- **Paperspace Gradient** - Professional cloud ML platform
- **Lightning.ai** - AI development platform

## 📋 Requirements

### Minimum Requirements
- 6GB VRAM (for 1.3B models)
- 8GB RAM
- 10GB storage space

### Recommended Requirements
- 12GB+ VRAM (for 14B models)
- 16GB+ RAM
- 20GB+ storage space

## 🔧 Platform-Specific Instructions

### Google Colab
1. Upload `OpusWan(1).ipynb`
2. Change runtime type to GPU (Runtime > Change runtime type > GPU)
3. Run all cells
4. Access via the generated public URL

### Kaggle
1. Create new notebook
2. Enable GPU (Settings > Accelerator > GPU)
3. Copy/paste cells from `OpusWan(1).ipynb`
4. Run cells sequentially

### RunPod
1. Create pod with PyTorch template
2. Upload notebook via JupyterLab
3. Run notebook or use terminal setup
4. Access via provided URLs

### Vast.ai
1. Rent GPU instance with Jupyter
2. Upload notebook
3. Ensure proper port forwarding for Gradio
4. Run notebook

## ⚡ Performance Tips

### For Low VRAM (6-8GB)
- Use 1.3B models only
- Enable fp16 mode
- Use conservative TeaCache settings

### For High VRAM (16GB+)
- Use 14B models for best quality
- Enable SageAttention for speed
- Use higher TeaCache multipliers

## 🔐 Security Notes

- The notebook uses `--share` flag for public access
- Generated URLs are temporary and expire after session
- For production use, consider proper authentication

## 🐛 Troubleshooting

### Common Issues

**"CUDA out of memory"**
- Switch to 1.3B models
- Reduce batch size
- Enable fp16 mode

**"No module named 'xxx'"**
- Ensure all cells in setup section are run
- Check internet connection for package downloads

**"Repository not found"**
- Check GitHub repository URL is correct
- Ensure repository is public

**"Gradio share failed"**
- Try refreshing the cell
- Check internet connection
- Use ngrok as alternative

## 📞 Support

For issues and support:
1. Check the troubleshooting section above
2. Review the main README.md
3. Check existing GitHub issues
4. Create new issue with full error logs

## 🔄 Updates

The notebook automatically clones the latest version. To force update:
- Set `FORCE_CLEAN_INSTALL = True` in the configuration section
- Or manually delete the workspace and re-run

---

**Happy video generating! 🎬**