# WanGP - Complete Video Generation Platform

**The Ultimate AI Video Generation Tool - Text2Video, Image2Video, VACE ControlNet & More**

WanGP is a comprehensive platform for AI video generation that supports multiple state-of-the-art models and advanced features like motion transfer, object injection, and video manipulation.

---

## 🌟 Features

### Core Capabilities
- **Text-to-Video**: Generate videos from text descriptions
- **Image-to-Video**: Animate static images with realistic motion
- **VACE ControlNet**: Advanced video manipulation (motion transfer, object injection, inpainting)
- **Multiple Model Support**: Wan 2.1, Hunyuan Video, LTX Video, and specialized models
- **LoRA System**: Custom style adaptations and character injection
- **Performance Optimizations**: Sage Attention, TeaCache, compilation support

### Supported Models

#### Wan 2.1 Text2Video Models
- **Wan 2.1 Text2Video 1.3B**: Fast generation, 6GB VRAM minimum
- **Wan 2.1 Text2Video 14B**: Highest quality, 12GB+ VRAM recommended
- **Wan Vace 1.3B/14B**: ControlNet for advanced video control
- **MoviiGen**: Experimental 1080p generation (20GB+ VRAM required)

#### Wan 2.1 Image-to-Video Models
- **Wan 2.1 Image2Video 14B**: Premium image animation
- **Wan Fun InP 1.3B/14B**: Fast and high-quality image-to-video
- **FLF2V**: Start/end frame specialist

#### Specialized Models
- **FantasySpeaking**: Talking head animation with voice sync
- **Phantom**: Person/object transfer between videos
- **Recam Master**: Viewpoint change specialist
- **Sky Reels v2**: "Infinite length" video generation
- **Hunyuan Video**: One of the best open-source T2V models
- **LTX Video 13B**: Long video support with fast 720p generation

---

## 🚀 Quick Start

### Cloud GPU Setup (Recommended)
For the easiest setup on cloud platforms like Google Colab, Kaggle, RunPod, etc.:

1. **Download the cloud setup notebook**: `wan2gp_cloud_setup.ipynb`
2. **Upload to your cloud platform**
3. **Run all cells** - it will auto-detect your environment and optimize settings
4. **Access the web interface** at the provided URL

### Local Installation

#### For RTX 10XX to RTX 40XX (Stable)
```bash
# Clone repository
git clone https://github.com/deepbeepmeep/Wan2GP.git
cd Wan2GP

# Create environment
conda create -n wan2gp python=3.10.9
conda activate wan2gp

# Install PyTorch
pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu124

# Install dependencies
pip install -r requirements.txt

# Optional performance optimizations
pip install triton sageattention==1.0.6 flash-attn==2.7.2.post1
```

#### For RTX 50XX (Beta)
```bash
# Same as above but with PyTorch 2.7.0
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu128
```

### Launch WanGP
```bash
# Basic launch
python wgp.py

# Optimized for your GPU (auto-detected)
python cloud_launcher.py --launch

# Specific modes
python wgp.py --t2v-1-3B    # Fast 1.3B model
python wgp.py --t2v-14B     # High-quality 14B model
python wgp.py --i2v         # Image-to-video
python wgp.py --vace-1-3B   # VACE ControlNet
```

---

## 📖 Complete Documentation

### Hardware Requirements

#### Minimum Requirements
- **GPU**: RTX 10XX series or newer (6GB VRAM)
- **RAM**: 8GB system memory
- **Storage**: 20GB free space for models
- **Python**: 3.10.9 (recommended)

#### Recommended Requirements
- **GPU**: RTX 30XX/40XX series (12GB+ VRAM)
- **RAM**: 16GB+ system memory
- **Storage**: 50GB+ for models and outputs

#### Performance Tiers
- **6-8GB VRAM**: Use 1.3B models with --fp16
- **12-16GB VRAM**: Use 14B models with standard settings
- **24GB+ VRAM**: Use 14B models with maximum performance settings

### Model Selection Guide

#### Choose Based on Your Needs

**For Speed (Low VRAM)**:
```bash
python wgp.py --t2v-1-3B --profile 4 --attention sdpa --fp16
```

**For Quality (High VRAM)**:
```bash
python wgp.py --t2v-14B --profile 3 --compile --attention sage2 --teacache 2.0
```

**For Advanced Control**:
```bash
python wgp.py --vace-14B --attention sage --compile
```

#### Model Capabilities Comparison

| Model | Size | VRAM | Speed | Quality | Special Features |
|-------|------|------|-------|---------|-----------------|
| Wan T2V 1.3B | 1.3B | 6GB | Fast | Good | General purpose |
| Wan T2V 14B | 14B | 12GB+ | Slow | Excellent | Best quality |
| Wan I2V 14B | 14B | 12GB+ | Slow | Excellent | Image animation |
| VACE 1.3B | 1.3B | 6GB | Fast | Good | Motion transfer, injection |
| VACE 14B | 14B | 12GB+ | Slow | Excellent | Advanced control |
| Hunyuan Video | Large | 10GB+ | Medium | Excellent | Identity preservation |
| LTX Video | 13B | 8GB+ | Fast | Good | Long videos |

### Command Line Reference

#### Basic Usage
```bash
# Default launch 
python wgp.py

# Specific model modes
python wgp.py --i2v           # Image-to-video
python wgp.py --t2v           # Text-to-video (default)
python wgp.py --t2v-14B       # 14B text-to-video model
python wgp.py --t2v-1-3B      # 1.3B text-to-video model
python wgp.py --i2v-14B       # 14B image-to-video model
python wgp.py --i2v-1-3B      # 1.3B image-to-video model
python wgp.py --vace-1-3B     # VACE ControlNet 1.3B model
python wgp.py --vace-14B      # VACE ControlNet 14B model
```

#### Performance Options
```bash
--quantize-transformer BOOL   # Enable/disable transformer quantization (default: True)
--compile                     # Enable PyTorch compilation (requires Triton)
--attention MODE              # Force attention mode: sdpa, flash, sage, sage2
--profile NUMBER              # Performance profile 1-5 (default: 4)
--preload NUMBER              # Preload N MB of diffusion model in VRAM
--fp16                        # Force fp16 instead of bf16 models
--gpu DEVICE                  # Run on specific GPU device (e.g., "cuda:1")
--teacache MULTIPLIER         # TeaCache speed multiplier: 0, 1.5, 1.75, 2.0, 2.25, 2.5
```

#### Performance Profiles
- **Profile 1**: Load entire model in VRAM, keep unused models in RAM
- **Profile 2**: Load model parts as needed, keep unused models in RAM
- **Profile 3**: Load entire model in VRAM (requires 24GB for 14B model)
- **Profile 4**: Default and recommended, most flexible option
- **Profile 5**: Minimum RAM usage

#### Server Options
```bash
--listen                      # Accept connections from network
--server-port PORT            # Set server port (default: 7860)
--share                       # Create shareable Gradio link
--open-browser               # Auto-open browser
--theme THEME                # UI theme
--lock-config                # Lock configuration for public use
```

#### LoRA Configuration
```bash
--lora-dir PATH              # Path to Wan t2v loras directory
--lora-dir-i2v PATH          # Path to Wan i2v loras directory
--lora-dir-hunyuan PATH      # Path to Hunyuan t2v loras directory
--lora-dir-hunyuan-i2v PATH  # Path to Hunyuan i2v loras directory
--lora-dir-ltxv PATH         # Path to LTX Video loras directory
--lora-preset PRESET         # Load lora preset file (.lset) on startup
--check-loras                # Filter incompatible loras (slower startup)
```

#### Example Commands
```bash
# High-performance setup with compilation
python wgp.py --compile --attention sage2 --profile 3

# Low VRAM setup
python wgp.py --t2v-1-3B --profile 4 --attention sdpa --fp16

# Network accessible server
python wgp.py --listen --server-port 8080 --share

# Maximum performance (requires high-end GPU)
python wgp.py --compile --attention sage2 --profile 3 --preload 2000 --teacache 2.0
```

### LoRA System Guide

#### Directory Structure
```
loras/                    # General t2v loras
├── 1.3B/                # Loras for 1.3B models
└── 14B/                 # Loras for 14B models

loras_i2v/               # Image-to-video loras
loras_hunyuan/           # Hunyuan Video t2v loras
loras_hunyuan_i2v/       # Hunyuan Video i2v loras
loras_ltxv/              # LTX Video loras
```

#### Using LoRAs

1. **Place LoRA files** in the appropriate directory
2. **Launch WanGP** with LoRA support
3. **In Advanced Tab**, select the "Loras" section
4. **Check the LoRAs** you want to activate
5. **Set multipliers** for each LoRA (default is 1.0)

#### LoRA Multipliers

**Simple Multipliers**:
```
1.2 0.8
```
- First LoRA: 1.2 strength
- Second LoRA: 0.8 strength

**Time-based Multipliers**:
```
0.9,0.8,0.7
1.2,1.1,1.0
```
- Dynamic strength changes over generation steps

#### LoRA Presets

Create preset files with `.lset` extension:
```
# Use the keyword "ohnvx" to trigger the lora
A ohnvx character is driving a car through the city
```

Load presets:
```bash
python wgp.py --lora-preset mypreset.lset
```

#### CausVid LoRA (Video Generation Accelerator)

CausVid enables 4-12 step generation with 2x speed improvement:

1. **Download CausVid LoRA**:
   ```
   https://huggingface.co/Kijai/WanVideo_comfy/blob/main/Wan21_CausVid_14B_T2V_lora_rank32.safetensors
   ```
2. **Place in `loras/` directory**
3. **Enable in LoRA section**
4. **Use 4-12 steps** for generation
5. **Set strength to 0.8-1.2**

### VACE ControlNet Guide

VACE enables advanced video manipulation including motion transfer, object injection, and video inpainting.

#### Key Features
- **Motion Transfer**: Transfer motion from one video to another
- **Object Injection**: Insert people or objects into scenes
- **Video Inpainting**: Fill masked areas with new content
- **Video Outpainting**: Extend video boundaries
- **Character Animation**: Animate characters with reference motion

#### Input Types

**Control Video**:
- Transfer motion or depth information
- Use first N frames and extrapolate the rest
- Perform inpainting with grey color (127) as mask

**Reference Images**:
- Background/setting for the video
- People or objects to inject
- Replace complex backgrounds with white for better integration

**Video Mask**:
- Black areas: keep original content
- White areas: replace with generated content
- Perfect for precise inpainting/outpainting

#### Common Use Cases

**Motion Transfer**:
```
Reference Images: Your character
Control Video: Person performing desired motion
Text Prompt: Describe your character and the action
```

**Object Injection**:
```
Reference Images: The people/objects to inject
Text Prompt: Describe the scene and explicitly mention injected elements
```

**Character Animation**:
```
Control Video: Video of person moving
Text Prompt: Detailed description of your character
```

#### Matanyone Tool Integration

WanGP includes the Matanyone tool for creating control videos and masks:

1. **Load video** in Matanyone
2. **Click on the face** in the first frame
3. **Create mask** for the face
4. **Generate video matting** with "Generate Video Matting"
5. **Export** to VACE with "Export to current Video Input and Video Mask"
6. **Load replacement** face image in Reference Images field

#### Recommended Settings
- **Skip Layer Guidance**: Turn ON for better results
- **Riflex option**: Enable for videos up to 7 seconds
- **Frame count**: Up to 7 seconds works best

### Generation Tips and Best Practices

#### Text-to-Video Prompts

**Effective Prompt Structure**:
```
[Subject] [Action] [Setting] [Style/Quality] [Camera/Lighting]
```

**Examples**:
```
"A cat walking through a sunny garden, cinematic shot, golden hour lighting"
"Cinematic shot of waves crashing on rocks at sunset, slow motion, dramatic lighting"
"A person dancing in the rain, close-up shot, soft lighting, artistic style"
```

**Prompt Tips**:
- Be descriptive but concise
- Include camera angles ("close-up", "wide shot", "cinematic")
- Mention lighting ("golden hour", "soft lighting", "dramatic")
- Specify motion ("slow motion", "fast paced", "gentle movement")
- Add quality terms ("cinematic", "professional", "artistic")

#### Generation Settings

**For Speed**:
- Use 1.3B models
- 10-15 steps
- Enable TeaCache
- Use SDPA attention

**For Quality**:
- Use 14B models
- 20-30 steps
- Disable TeaCache
- Use Sage attention
- Higher resolution

**Recommended Settings by Use Case**:

| Use Case | Model | Steps | TeaCache | Attention | Profile |
|----------|-------|-------|----------|-----------|---------|
| Quick Preview | 1.3B | 10-15 | 2.0 | SDPA | 4 |
| Standard Quality | 14B | 20-25 | 1.5 | Sage | 4 |
| Maximum Quality | 14B | 30+ | 0 | Sage2 | 3 |
| Low VRAM | 1.3B | 15-20 | 1.5 | SDPA | 4 |

### Performance Optimization

#### Attention Mechanisms

**SDPA (Default)**:
- Available by default with PyTorch
- Good compatibility with all GPUs
- Moderate performance

**Sage Attention**:
- 30% faster than SDPA
- Requires Triton installation
- Small quality cost
- Installation: `pip install sageattention==1.0.6`

**Sage2 Attention**:
- 40% faster than SDPA
- Requires Triton and SageAttention 2.x
- Best performance option
- More complex installation

**Flash Attention**:
- Good performance
- May require CUDA kernel compilation
- Complex to install on Windows

#### GPU-Specific Optimizations

**RTX 10XX/20XX Series**:
```bash
python wgp.py --attention sdpa --profile 4 --teacache 1.5 --fp16
```

**RTX 30XX/40XX Series**:
```bash
python wgp.py --compile --attention sage --profile 3 --teacache 2.0
```

**RTX 50XX Series**:
```bash
python wgp.py --attention sage --profile 4 --fp16
```

#### Memory Management

**VRAM Optimization**:
- Use appropriate model size for your VRAM
- Enable `--fp16` for lower precision
- Adjust `--profile` setting
- Use `--preload 0` for minimum VRAM usage

**RAM Optimization**:
- Limit reserved memory with `--perc-reserved-mem-max 0.3`
- Use `--profile 5` for minimal RAM usage
- Enable system swap file

### Installation Guide

#### System Requirements

**Python Version**: 3.10.9 (strongly recommended)
**CUDA Support**: Required for GPU acceleration
**Operating Systems**: Windows, Linux, macOS (limited GPU support)

#### Step-by-Step Installation

**1. Environment Setup**:
```bash
# Using Conda (recommended)
conda create -n wan2gp python=3.10.9
conda activate wan2gp

# Using venv
python3.10 -m venv wan2gp
source wan2gp/bin/activate  # Linux/Mac
# or
wan2gp\Scripts\activate     # Windows
```

**2. Repository Clone**:
```bash
git clone https://github.com/deepbeepmeep/Wan2GP.git
cd Wan2GP
```

**3. PyTorch Installation**:

For RTX 10XX-40XX (Stable):
```bash
pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu124
```

For RTX 50XX (Beta):
```bash
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu128
```

**4. Dependencies**:
```bash
pip install -r requirements.txt
```

**5. Performance Optimizations** (Optional):

Triton (for compilation):
```bash
# Windows
pip install triton-windows

# Linux
pip install triton
```

Sage Attention:
```bash
pip install sageattention==1.0.6
```

Flash Attention:
```bash
pip install flash-attn==2.7.2.post1
```

### Cloud Platform Setup

#### Universal Cloud Setup

Use the provided `wan2gp_cloud_setup.ipynb` notebook for automatic setup on any cloud platform:

1. **Upload notebook** to your cloud service
2. **Ensure GPU runtime** is selected
3. **Run all cells** - automatic detection and optimization
4. **Access web interface** via provided URLs

#### Platform-Specific Notes

**Google Colab**:
- Select GPU runtime (Runtime → Change runtime type → GPU)
- Free tier has session limits
- Pro/Pro+ recommended for longer sessions

**Kaggle**:
- Enable GPU in notebook settings
- Enable internet access if needed
- 30 hours/week GPU quota on free tier

**RunPod**:
- Use provided RunPod template
- Choose appropriate GPU (RTX A5000+ recommended)
- Persistent storage recommended

**Paperspace Gradient**:
- Select GPU instance (P4000 or better)
- Use machine learning templates

**AWS SageMaker**:
- Create notebook instance with GPU
- ml.p3.2xlarge or better recommended

#### Docker Deployment

Use the provided Dockerfile for containerized deployment:

```bash
# Build image
docker build -t wan2gp .

# Run container
docker run --gpus all -p 7860:7860 wan2gp
```

### Troubleshooting

#### Installation Issues

**PyTorch Installation Problems**:
```bash
# Check CUDA version
nvidia-smi

# Install matching PyTorch version
# For CUDA 12.4 (RTX 10XX-40XX)
pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu124

# For CUDA 12.8 (RTX 50XX)
pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu128
```

**Python Version Issues**:
```bash
# Ensure Python 3.10.9
python --version
conda create -n wan2gp python=3.10.9
```

**Dependency Installation Failures**:
- Update pip: `pip install --upgrade pip`
- Install Visual Studio Build Tools (Windows)
- Use pre-compiled wheels when available
- Fallback to basic attention modes

#### Memory Issues

**CUDA Out of Memory**:

During model loading:
```bash
# Use smaller model
python wgp.py --t2v-1-3B

# Enable quantization
python wgp.py --quantize-transformer True

# Use memory-efficient profile
python wgp.py --profile 4

# Reduce preloaded model size
python wgp.py --preload 0
```

During video generation:
- Reduce frame count (shorter videos)
- Lower resolution in advanced settings
- Use lower batch size
- Clear GPU cache between generations

**System RAM Issues**:
```bash
# Limit reserved memory
python wgp.py --perc-reserved-mem-max 0.3

# Use minimal RAM profile
python wgp.py --profile 5
```

#### Performance Issues

**Slow Generation Speed**:
```bash
# Enable compilation (requires Triton)
python wgp.py --compile

# Use faster attention
python wgp.py --attention sage2

# Enable TeaCache
python wgp.py --teacache 2.0

# Use high-performance profile
python wgp.py --profile 3
```

**Attention Mechanism Issues**:

Sage Attention not working:
1. Check Triton installation: `python -c "import triton; print(triton.__version__)"`
2. Clear Triton cache: `rm -rf ~/.triton` (Linux) or `rmdir /s %USERPROFILE%\.triton` (Windows)
3. Fallback: `python wgp.py --attention sdpa`

**Model-Specific Issues**:

LoRA problems:
- Enable `--check-loras` to filter incompatible LoRAs
- Verify LoRA is in correct directory
- Check LoRA file format (`.safetensors` recommended)

Model download issues:
- Ensure stable internet connection
- Check available disk space
- Clear Hugging Face cache: `~/.cache/huggingface/`

#### Error Codes and Solutions

**Common Error Messages**:

`"CUDA out of memory"`:
- Use smaller model or reduce settings
- Add `--fp16` flag
- Increase system swap file

`"No module named 'triton'"`:
- Install appropriate Triton version
- Skip compilation: remove `--compile` flag

`"Failed to load model"`:
- Check internet connection
- Clear model cache
- Verify disk space

`"Port already in use"`:
- Change port: `--server-port 7861`
- Kill existing processes: `pkill -f wgp.py`

### Advanced Features

#### Custom Model Training

WanGP supports LoRA training for custom styles and characters:

1. **Prepare dataset** (images/videos with consistent style)
2. **Use training script** (coming soon)
3. **Place trained LoRA** in appropriate directory
4. **Load in interface** or via command line

#### API Integration

Launch WanGP as an API server:
```bash
python wgp.py --api --listen --server-port 7860
```

Access endpoints:
- `/api/generate` - Generate video
- `/api/models` - List available models
- `/api/status` - Server status

#### Batch Processing

Process multiple prompts:
```bash
python batch_generate.py --input prompts.txt --output videos/
```

#### Custom Workflows

Create automated pipelines:
1. **Text-to-Video** generation
2. **Post-processing** with video editing tools
3. **LoRA style** application
4. **Batch export** in multiple formats

### Community and Support

#### Getting Help

**Documentation**:
- Complete guides in `/docs` folder
- Troubleshooting section for common issues
- Command reference for all options

**Community**:
- Discord server for real-time help
- GitHub Issues for bug reports
- Reddit community for sharing results

**Contributing**:
- Report bugs via GitHub Issues
- Submit feature requests
- Contribute LoRAs and models
- Help with documentation

#### Latest Updates

**May 28, 2025**: WanGP v5.41
- Support for AccVideo LoRA (2x speed boost)
- Hunyuan Video Avatar Support
- Reduced VRAM requirements

**May 26, 2025**: WanGP v5.3
- Video settings extraction and reuse
- Improved VACE transitions
- Enhanced Matanyone integration

**May 20, 2025**: WanGP v5.2
- CausVid LoRA support (4-12 step generation)
- MoviiGen experimental 1080p support

See full changelog in `docs/CHANGELOG.md`

---

## 📂 File Structure

```
Wan2GP/
├── docs/                          # Complete documentation
│   ├── GETTING_STARTED.md         # Quick start guide
│   ├── INSTALLATION.md            # Detailed installation
│   ├── CLI.md                     # Command line reference
│   ├── MODELS.md                  # Model overview
│   ├── LORAS.md                   # LoRA system guide
│   ├── VACE.md                    # VACE ControlNet guide
│   ├── TROUBLESHOOTING.md         # Common issues
│   └── CHANGELOG.md               # Version history
├── cloud_setup/                   # Cloud deployment files
│   ├── wan2gp_cloud_setup.ipynb   # Universal cloud notebook
│   ├── cloud_launcher.py          # Auto-optimizing launcher
│   ├── setup_cloud.sh             # Automated setup script
│   ├── Dockerfile                 # Container deployment
│   ├── docker-compose.yml         # Docker Compose setup
│   └── platform_templates/        # Cloud service templates
├── loras/                         # LoRA files directory
├── models/                        # Downloaded models cache
├── outputs/                       # Generated videos
├── wgp.py                         # Main application
├── requirements.txt               # Python dependencies
└── README.md                      # Basic readme
```

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Launch with auto-optimization
python cloud_launcher.py --launch

# Basic modes
python wgp.py --t2v-1-3B    # Fast text-to-video
python wgp.py --i2v-14B     # High-quality image-to-video
python wgp.py --vace-1-3B   # Advanced control

# Performance optimized
python wgp.py --compile --attention sage2 --teacache 2.0

# Low VRAM mode
python wgp.py --t2v-1-3B --fp16 --profile 4
```

### Hardware Recommendations
- **Budget**: RTX 3060 12GB → Use 1.3B models
- **Mainstream**: RTX 4070/4080 → Use 14B models
- **Enthusiast**: RTX 4090/A6000 → Maximum settings
- **Professional**: Multiple GPUs → Distributed processing

### Performance Tips
1. **Use appropriate model** for your VRAM
2. **Enable TeaCache** for 2x speed boost
3. **Use Sage attention** for 30% speed improvement
4. **Compile models** with Triton for additional speed
5. **Adjust step count** for speed/quality balance

---

## 📄 License and Credits

**License**: Check repository for current license terms
**Credits**: Built on top of various open-source AI models and libraries
**Contributing**: See CONTRIBUTING.md for guidelines

---

**For the latest updates and detailed documentation, visit the [official repository](https://github.com/deepbeepmeep/Wan2GP)**