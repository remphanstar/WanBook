#!/usr/bin/env python3
"""
WanGP Cloud Launcher - Fixed Version
Universal launcher for any cloud GPU platform
"""

import os
import sys
import subprocess
import platform

class WanGPCloudLauncher:
    def __init__(self):
        self.platform = self.detect_platform()
        self.gpu_info = self.get_gpu_info()
        self.optimal_settings = self.determine_optimal_settings()
    
    def detect_platform(self):
        """Detect cloud platform"""
        if 'COLAB_GPU' in os.environ:
            return 'colab'
        elif 'KAGGLE_KERNEL_RUN_TYPE' in os.environ:
            return 'kaggle'
        elif 'RUNPOD_POD_ID' in os.environ:
            return 'runpod'
        else:
            return 'generic'
    
    def get_gpu_info(self):
        """Get GPU information"""
        try:
            import torch
            if torch.cuda.is_available():
                return {
                    'name': torch.cuda.get_device_name(0),
                    'memory_gb': torch.cuda.get_device_properties(0).total_memory / 1024**3,
                }
        except ImportError:
            pass
        return {'name': 'Unknown', 'memory_gb': 0}
    
    def determine_optimal_settings(self):
        """Determine optimal settings based on hardware"""
        memory = self.gpu_info['memory_gb']
        gpu_name = self.gpu_info['name'].lower()
        
        settings = {
            'model': '--t2v-1-3B',
            'profile': '4',
            'attention': 'sdpa',
            'extra_flags': []
        }
        
        # Memory-based optimizations
        if memory >= 24:
            settings['model'] = '--t2v-14B'
            settings['profile'] = '3'
            settings['extra_flags'].extend(['--preload', '2000'])
        elif memory >= 12:
            settings['model'] = '--t2v-14B'
            settings['extra_flags'].extend(['--preload', '1000'])
        elif memory >= 8:
            settings['extra_flags'].extend(['--preload', '500'])
        else:
            settings['extra_flags'].extend(['--preload', '0', '--fp16'])
        
        # GPU generation optimizations
        if 'rtx 50' in gpu_name:
            settings['extra_flags'].append('--fp16')
        elif any(x in gpu_name for x in ['rtx 30', 'rtx 40', 'a100', 'v100']):
            settings['extra_flags'].extend(['--teacache', '2.0'])
        elif any(x in gpu_name for x in ['rtx 20', 'rtx 10']):
            settings['extra_flags'].extend(['--teacache', '1.5'])
        
        # Try advanced features
        try:
            import sageattention
            settings['attention'] = 'sage'
        except ImportError:
            pass
        
        try:
            import triton
            settings['extra_flags'].append('--compile')
        except ImportError:
            pass
        
        return settings
    
    def create_launch_command(self):
        """Create properly formatted launch command"""
        cmd = [sys.executable, 'wgp.py']
        
        # Add model
        cmd.append(self.optimal_settings['model'])
        
        # Add profile and attention with proper separation
        cmd.extend(['--profile', self.optimal_settings['profile']])
        cmd.extend(['--attention', self.optimal_settings['attention']])
        
        # Add server options
        cmd.extend(['--listen', '--server-port', '7860', '--share'])
        
        # Process extra flags properly
        i = 0
        extra_flags = self.optimal_settings['extra_flags']
        while i < len(extra_flags):
            flag = extra_flags[i]
            if flag.startswith('--') and i + 1 < len(extra_flags) and not extra_flags[i + 1].startswith('--'):
                cmd.extend([flag, extra_flags[i + 1]])
                i += 2
            else:
                cmd.append(flag)
                i += 1
        
        return cmd
    
    def launch(self):
        """Launch WanGP with optimal settings"""
        cmd = self.create_launch_command()
        
        print("🚀 Launching WanGP...")
        print(f"GPU: {self.gpu_info['name']}")
        print(f"VRAM: {self.gpu_info['memory_gb']:.1f} GB")
        print(f"Command: {' '.join(cmd)}")
        print("=" * 60)
        
        try:
            subprocess.run(cmd, check=True)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down WanGP...")
        except Exception as e:
            print(f"❌ Launch failed: {e}")
            print("💡 Try minimal: python wgp.py --listen --share")

def main():
    if not os.path.exists('wgp.py'):
        if os.path.exists('Wan2GP/wgp.py'):
            os.chdir('Wan2GP')
        else:
            print("❌ wgp.py not found. Please run from Wan2GP directory")
            return
    
    launcher = WanGPCloudLauncher()
    
    if '--launch' in sys.argv:
        launcher.launch()
    else:
        print("🎯 Ready to launch!")
        print("Run: python cloud_launcher.py --launch")

if __name__ == "__main__":
    main()
