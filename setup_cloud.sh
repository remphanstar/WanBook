#!/bin/bash
# WanGP Cloud Setup Script
# Platform-agnostic setup for any cloud GPU service

set -e

echo "🚀 WanGP Cloud Setup Script"
echo "=========================="

# Detect environment
detect_environment() {
    if [ -n "$COLAB_GPU" ]; then
        echo "colab"
    elif [ -n "$KAGGLE_KERNEL_RUN_TYPE" ]; then
        echo "kaggle"
    elif [ -n "$SM_TRAINING_ENV" ]; then
        echo "sagemaker"
    elif [ -n "$PAPERSPACE_NOTEBOOK_REPO_ID" ]; then
        echo "paperspace"
    elif [ -n "$RUNPOD_POD_ID" ]; then
        echo "runpod"
    else
        echo "generic"
    fi
}

ENV=$(detect_environment)
echo "🔍 Detected environment: $ENV"

# Check GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✅ GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
else
    echo "⚠️  No GPU detected!"
fi

# Update system packages
echo "📦 Updating system packages..."
if [ "$ENV" != "colab" ] && [ "$ENV" != "kaggle" ]; then
    sudo apt-get update -qq
    sudo apt-get install -y git wget curl ffmpeg libgl1-mesa-glx libglib2.0-0
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "🐍 Python version: $PYTHON_VERSION"

if [ "$PYTHON_VERSION" != "3.10" ]; then
    echo "⚠️  Warning: Python 3.10 is recommended"
fi

# Install/upgrade pip
echo "📦 Installing pip packages..."
python3 -m pip install --upgrade pip

# Determine PyTorch version based on GPU
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null || echo "unknown")
if [[ "$GPU_NAME" == *"RTX 50"* ]]; then
    echo "🔧 Installing PyTorch 2.7.0 for RTX 50XX series..."
    pip install torch==2.7.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu128
else
    echo "🔧 Installing PyTorch 2.6.0 for RTX 10XX-40XX series..."
    pip install torch==2.6.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu124
fi

# Clone repository
if [ ! -d "Wan2GP" ]; then
    echo "📥 Cloning WanGP repository..."
    git clone https://github.com/deepbeepmeep/Wan2GP.git
fi

cd Wan2GP

# Install requirements
echo "📦 Installing WanGP requirements..."
pip install -r requirements.txt

# Install performance optimizations
echo "⚡ Installing performance optimizations..."
if [ "$(uname)" == "Linux" ]; then
    pip install triton || echo "Triton installation failed"
else
    pip install triton-windows || echo "Triton installation failed"
fi

pip install sageattention==1.0.6 || echo "SageAttention installation failed"
pip install flash-attn==2.7.2.post1 || echo "Flash Attention installation failed"

# Create launch script
echo "📝 Creating launch script..."
cat > launch.sh << 'EOF'
#!/bin/bash
# WanGP Launch Script

# Determine optimal settings based on GPU memory
GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -n1)
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -n1)

echo "GPU: $GPU_NAME"
echo "VRAM: ${GPU_MEMORY}MB"

# Base command
CMD="python wgp.py --listen --server-port 7860 --share"

# Memory-based model selection
if [ "$GPU_MEMORY" -gt 20000 ]; then
    CMD="$CMD --t2v-14B --profile 3 --compile --attention sage --teacache 2.0"
    echo "🚀 High-end configuration (24GB+ VRAM)"
elif [ "$GPU_MEMORY" -gt 10000 ]; then
    CMD="$CMD --t2v-14B --profile 4 --attention sage --teacache 1.5"
    echo "⚡ Mid-range configuration (12GB+ VRAM)"
else
    CMD="$CMD --t2v-1-3B --profile 4 --attention sdpa --fp16"
    echo "💡 Low VRAM configuration (6-10GB VRAM)"
fi

# GPU-specific optimizations
if [[ "$GPU_NAME" == *"RTX 50"* ]]; then
    CMD="$CMD --fp16"
fi

echo "Launching with command: $CMD"
echo "================================"

# Launch WanGP
exec $CMD
EOF

chmod +x launch.sh

# Create quick commands file
cat > quick_commands.txt << 'EOF'
# WanGP Quick Launch Commands

# Optimized launch (auto-detected settings)
./launch.sh

# Text-to-Video modes
python wgp.py --t2v --listen --share                    # Default T2V
python wgp.py --t2v-1-3B --listen --share              # Fast 1.3B model
python wgp.py --t2v-14B --listen --share               # High-quality 14B model

# Image-to-Video modes  
python wgp.py --i2v --listen --share                    # Default I2V
python wgp.py --i2v-1-3B --listen --share              # Fast I2V
python wgp.py --i2v-14B --listen --share               # High-quality I2V

# VACE ControlNet (advanced)
python wgp.py --vace-1-3B --listen --share             # VACE 1.3B
python wgp.py --vace-14B --listen --share              # VACE 14B

# Performance optimized
python wgp.py --compile --attention sage2 --teacache 2.0 --listen --share

# Low VRAM mode (6GB)
python wgp.py --t2v-1-3B --profile 4 --attention sdpa --fp16 --listen --share

# High VRAM mode (24GB+)
python wgp.py --t2v-14B --profile 3 --compile --attention sage2 --teacache 2.0 --preload 2000 --listen --share
EOF

echo "✅ Setup complete!"
echo ""
echo "🚀 To launch WanGP:"
echo "   cd Wan2GP && ./launch.sh"
echo ""
echo "📖 Quick commands available in: Wan2GP/quick_commands.txt"
echo "🌐 Access the web interface at: http://localhost:7860"
echo ""
echo "💡 First launch will download models (10-20 minutes)"