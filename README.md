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

1. **Download the cloud setup notebook**: `OpusWan(1).ipynb`
2. **Upload to your cloud platform**
3. **Run all cells** - it will auto-detect your environment and optimize settings
4. **Access the web interface** at the provided URL

### Local Installation

#### For RTX 10XX to RTX 40XX (Stable)
```bash
# Clone repository
git clone https://github.com/remphanstar/WanBook.git
cd WanBook

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

1. **Download CausVid LoRA**: [Download from Hugging Face](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan21_CausVid_14B_T2V_lora_rank32.safetensors)
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

**Example Good Prompts**:
- "A majestic golden eagle soaring through snow-capped mountains, cinematic lighting, 4K quality"
- "A young woman walking through a bustling Tokyo street at night, neon lights reflecting on wet pavement"
- "A steam locomotive crossing a stone bridge over a misty valley, vintage film aesthetic"

**Prompt Tips**:
- Be specific about movement and action
- Include camera angles and lighting descriptions
- Mention quality terms: "cinematic", "4K", "high quality"
- Describe the environment and atmosphere
- Use artistic style references when appropriate

#### Performance Optimization

**Low VRAM (6-8GB)**:
- Use 1.3B models
- Enable `--fp16` mode
- Set `--profile 4` or `--profile 5`
- Use `--teacache 1.5`
- Lower resolution (480p)

**Medium VRAM (8-12GB)**:
- Mix of 1.3B and 14B models
- Standard settings with `--profile 4`
- Use `--teacache 2.0`
- 720p resolution

**High VRAM (16GB+)**:
- Use 14B models freely
- Enable `--compile` for speed
- Use `--attention sage2`
- Set `--profile 3`
- Use `--teacache 2.5`
- 1080p+ resolution

#### Troubleshooting

**Common Issues**:

1. **Out of Memory Errors**:
   - Reduce batch size
   - Use smaller models (1.3B instead of 14B)
   - Enable `--fp16`
   - Lower resolution

2. **Slow Generation**:
   - Install SageAttention: `pip install sageattention`
   - Use TeaCache: `--teacache 2.0`
   - Enable compilation: `--compile`

3. **Poor Quality Results**:
   - Use 14B models if VRAM allows
   - Increase steps (20-30)
   - Improve prompt quality
   - Use appropriate LoRAs

4. **Connection Issues**:
   - Use `--share` for public URL
   - Check firewall settings
   - Try different port: `--server-port 8080`

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Thanks to the Wan 2.1 team for the amazing models
- Hunyuan Video team for their excellent T2V model
- The open-source AI community for continuous innovation

**For the latest updates and detailed documentation, visit the [official repository](https://github.com/remphanstar/WanBook)**