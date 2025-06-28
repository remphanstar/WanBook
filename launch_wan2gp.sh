#!/bin/bash
# Fixed WanGP launcher with proper argument separation

# Detect GPU memory
GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1)
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -n1)

echo "🚀 WanGP Launcher"
echo "GPU: $GPU_NAME"
echo "VRAM: ${GPU_MEMORY}MB"

# Build command based on available memory
if [ "$GPU_MEMORY" -gt 20000 ]; then
    MODEL="--t2v-14B"
    PROFILE="3"
    PRELOAD="--preload 2000"
elif [ "$GPU_MEMORY" -gt 10000 ]; then
    MODEL="--t2v-14B" 
    PROFILE="4"
    PRELOAD="--preload 1000"
else
    MODEL="--t2v-1-3B"
    PROFILE="4"
    PRELOAD="--preload 0 --fp16"
fi

# Check if sage attention is available
if python -c "import sageattention" 2>/dev/null; then
    ATTENTION="sage"
else
    ATTENTION="sdpa"
fi

# Check if triton is available
if python -c "import triton" 2>/dev/null; then
    COMPILE="--compile"
else
    COMPILE=""
fi

# Build and execute command with proper argument separation
echo "Starting WanGP..."
exec python wgp.py $MODEL --profile $PROFILE --attention $ATTENTION --listen --server-port 7860 --share $PRELOAD $COMPILE
