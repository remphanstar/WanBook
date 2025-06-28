#!/usr/bin/env python3
"""
WanGP Auto-Launch Script for Cloud GPU Platforms
Fixed version with environment variable handling
"""

import os
import sys
import subprocess
import torch

# Set environment variables to prevent common errors
if 'XDG_RUNTIME_DIR' not in os.environ:
    import getpass
    runtime_dir = f"/tmp/runtime-{getpass.getuser()}"
    os.environ['XDG_RUNTIME_DIR'] = runtime_dir
    if not os.path.exists(runtime_dir):
        os.makedirs(runtime_dir, mode=0o700)
    print(f"✅ Set XDG_RUNTIME_DIR to {runtime_dir}")

# Fix ALSA warnings
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['ALSA_CONFIG_PATH'] = '/dev/null'
print("✅ Configured audio to use dummy drivers")

def get_optimal_settings():
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    gpu_name = torch.cuda.get_device_name(0).lower()
    
    settings = {
        'model': '--t2v-1-3B',  # Default to smaller model
        'profile': '4',         # Just the value, not the flag
        'attention': 'sdpa',    # Just the value, not the flag
        'extra_flags': []       # Will be processed correctly
    }
    
    # GPU-specific optimizations
    if gpu_memory >= 24:
        settings['model'] = '--t2v-14B'  # Use larger model
        settings['profile'] = '3'  # High performance
        settings['extra_flags'].extend(['--preload', '2000'])
    elif gpu_memory >= 12:
        settings['model'] = '--t2v-14B'  # Can handle 14B model
        settings['extra_flags'].extend(['--preload', '1000'])
    elif gpu_memory >= 8:
        settings['extra_flags'].extend(['--preload', '500'])
    else:
        settings['extra_flags'].extend(['--preload', '0'])
        settings['extra_flags'].append('--fp16')
    
    # Try better attention if available
    try:
        import sageattention
        settings['attention'] = 'sage'
        print("✅ Using Sage Attention")
    except ImportError:
        print("ℹ️ Using default SDPA attention")
    
    # Enable compilation if Triton is available
    try:
        import triton
        settings['extra_flags'].append('--compile')
        print("✅ Compilation enabled")
    except ImportError:
        print("ℹ️ Compilation disabled (Triton not available)")
    
    # GPU generation specific settings
    if 'rtx 50' in gpu_name:
        settings['extra_flags'].append('--fp16')
    elif any(x in gpu_name for x in ['rtx 30', 'rtx 40', 'a100', 'v100']):
        settings['extra_flags'].extend(['--teacache', '2.0'])
    elif any(x in gpu_name for x in ['rtx 20', 'rtx 10', 't4']):
        settings['extra_flags'].extend(['--teacache', '1.5'])
        
    return settings

def main():
    settings = get_optimal_settings()
    
    # Build command with proper argument separation
    cmd = [sys.executable, "wgp.py"]
    cmd.append(settings['model'])
    cmd.extend(["--profile", settings['profile']])
    cmd.extend(["--attention", settings['attention']])
    cmd.extend(["--listen", "--server-port", "7860", "--share"])
    
    i = 0
    extra_flags = settings['extra_flags']
    while i < len(extra_flags):
        flag = extra_flags[i]
        if flag.startswith('--') and i + 1 < len(extra_flags) and not extra_flags[i + 1].startswith('--'):
            cmd.extend([flag, extra_flags[i + 1]])
            i += 2
        else:
            cmd.append(flag)
            i += 1
    
    print("Starting WanGP with command:")
    print(" ".join(cmd))
    print("\n" + "="*50)
    print("WanGP is starting up...")
    print("This may take a few minutes for first-time model downloads.")
    print("="*50 + "\n")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nShutting down WanGP...")
        print("Done!")

if __name__ == "__main__":
    main()
