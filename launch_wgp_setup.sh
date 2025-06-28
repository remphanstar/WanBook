#!/bin/bash
# WanGP Launch Script with Environment Fixes
# Fixed version that sets necessary environment variables

# Set XDG_RUNTIME_DIR to a permanent temporary directory if not already set
if [ -z "$XDG_RUNTIME_DIR" ]; then
    export XDG_RUNTIME_DIR="/tmp/runtime-$USER"
    if [ ! -d "$XDG_RUNTIME_DIR" ]; then
        mkdir -p "$XDG_RUNTIME_DIR"
        chmod 700 "$XDG_RUNTIME_DIR"
    fi
    echo "✅ Set XDG_RUNTIME_DIR to $XDG_RUNTIME_DIR"
fi

# Configure audio driver to dummy to bypass ALSA warnings in headless environments
export SDL_AUDIODRIVER=dummy
export ALSA_CONFIG_PATH=/dev/null
echo "✅ Configured audio to use dummy drivers"

# Detect GPU memory using nvidia-smi (assumes nvidia-smi is available)
GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1)
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits 2>/dev/null | head -n1)

echo "🚀 WanGP Launcher with Environment Fixes"
echo "GPU: $GPU_NAME"
echo "VRAM: ${GPU_MEMORY}MB"

# Adjust model and flags based on available GPU memory
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

# Check for sageattention module to set attention mode
if python -c "import sageattention" 2>/dev/null; then
    ATTENTION="sage"
else
    ATTENTION="sdpa"
fi

# Check for triton module to set compilation flag
if python -c "import triton" 2>/dev/null; then
    COMPILE="--compile"
else
    COMPILE=""
fi

# Optionally set teacache based on GPU memory
if [ "$GPU_MEMORY" -gt 10000 ]; then
    TEACACHE="--teacache 1.5"
else
    TEACACHE=""
fi

# Build the final launch command
CMD="python wgp.py $MODEL --profile $PROFILE --attention $ATTENTION --listen --server-port 7860 --share $PRELOAD $COMPILE $TEACACHE"

echo "Starting WanGP with the following command:"
echo "$CMD"
echo "============================================================"
echo "IMPORTANT NOTES:"
echo "• First launch will download models (this may take 10-20 minutes)"
echo "• The web interface will be available at the URLs shown below"
echo "• Use Ctrl+C to stop the server"
echo "============================================================"

# Execute the command
exec $CMD
