#!/usr/bin/env python3
"""
WanGP Cloud Launcher
Universal launcher for any cloud GPU platform
"""

import os
import sys
import subprocess
import json
import platform
import time
from pathlib import Path

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
        elif 'SM_TRAINING_ENV' in os.environ:
            return 'sagemaker'
        elif 'PAPERSPACE_NOTEBOOK_REPO_ID' in os.environ:
            return 'paperspace'
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
                    'count': torch.cuda.device_count(),
                    'cuda_version': torch.version.cuda
                }
        except ImportError:
            pass
        
        return {'name': 'Unknown', 'memory_gb': 0, 'count': 0, 'cuda_version': None}
    
    def determine_optimal_settings(self):
        """Determine optimal settings based on hardware"""
        memory = self.gpu_info['memory_gb']
        gpu_name = self.gpu_info['name'].lower()
        
        settings = {
            'model': '--t2v-1-3B',  # Safe default
            'profile': '--profile 4',
            'attention': '--attention sdpa',
            'extra_flags': ['--listen', '--server-port 7860', '--share']
        }
        
        # Memory-based optimizations
        if memory >= 24:
            settings['model'] = '--t2v-14B'
            settings['profile'] = '--profile 3'
            settings['extra_flags'].append('--preload 2000')
        elif memory >= 12:
            settings['model'] = '--t2v-14B'
            settings['extra_flags'].append('--preload 1000')
        elif memory >= 8:
            settings['extra_flags'].append('--preload 500')
        else:
            settings['extra_flags'].extend(['--preload 0', '--fp16'])
        
        # GPU generation optimizations
        if 'rtx 50' in gpu_name:
            settings['extra_flags'].append('--fp16')
        elif any(x in gpu_name for x in ['rtx 30', 'rtx 40', 'a100', 'v100']):
            settings['extra_flags'].append('--teacache 2.0')
        elif any(x in gpu_name for x in ['rtx 20', 'rtx 10']):
            settings['extra_flags'].append('--teacache 1.5')
        
        # Try advanced features
        try:
            import sageattention
            settings['attention'] = '--attention sage'
        except ImportError:
            pass
        
        try:
            import triton
            settings['extra_flags'].append('--compile')
        except ImportError:
            pass
        
        return settings
    
    def print_system_info(self):
        """Print system information"""
        print("🖥️  System Information")
        print("=" * 50)
        print(f"Platform: {self.platform}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"OS: {platform.platform()}")
        
        if self.gpu_info['name'] != 'Unknown':
            print(f"GPU: {self.gpu_info['name']}")
            print(f"VRAM: {self.gpu_info['memory_gb']:.1f} GB")
            print(f"CUDA: {self.gpu_info['cuda_version']}")
        else:
            print("GPU: Not detected")
        print("=" * 50)
    
    def setup_environment(self):
        """Setup environment-specific configurations"""
        if self.platform == 'colab':
            print("📱 Setting up Google Colab...")
            # Colab-specific setup
            subprocess.run(['nvidia-smi', '-pm', '1'], check=False)
        
        elif self.platform == 'kaggle':
            print("🏆 Setting up Kaggle...")
            print("⚠️  Ensure internet access is enabled in Kaggle settings")
        
        elif self.platform == 'paperspace':
            print("📄 Setting up Paperspace...")
            subprocess.run(['nvidia-smi', '-pm', '1'], check=False)
        
        print(f"✅ Environment setup complete for {self.platform}")
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Installing dependencies...")
        
        # Determine PyTorch version
        gpu_name = self.gpu_info['name'].lower()
        if 'rtx 50' in gpu_name:
            pytorch_cmd = [sys.executable, '-m', 'pip', 'install', 
                          'torch==2.7.0', 'torchvision', 'torchaudio', 
                          '--index-url', 'https://download.pytorch.org/whl/test/cu128']
        else:
            pytorch_cmd = [sys.executable, '-m', 'pip', 'install', 
                          'torch==2.6.0', 'torchvision', 'torchaudio', 
                          '--index-url', 'https://download.pytorch.org/whl/test/cu124']
        
        print("Installing PyTorch...")
        subprocess.run(pytorch_cmd, check=True)
        
        # Install requirements
        if Path('requirements.txt').exists():
            print("Installing WanGP requirements...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        
        # Performance optimizations
        print("Installing performance optimizations...")
        opt_packages = [
            ('triton' if platform.system() != 'Windows' else 'triton-windows', False),
            ('sageattention==1.0.6', False),
            ('flash-attn==2.7.2.post1', False)
        ]
        
        for package, required in opt_packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=required, capture_output=True)
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError:
                print(f"⚠️  {package} installation failed (optional)")
    
    def create_launch_script(self):
        """Create platform-specific launch script"""
        cmd_parts = ['python', 'wgp.py']
        cmd_parts.extend([
            self.optimal_settings['model'],
            self.optimal_settings['profile'], 
            self.optimal_settings['attention']
        ])
        cmd_parts.extend(self.optimal_settings['extra_flags'])
        
        script_content = f'''#!/usr/bin/env python3
"""
Auto-generated WanGP launcher for {self.platform}
"""
import subprocess
import sys

def main():
    cmd = {cmd_parts}
    print("🚀 Starting WanGP...")
    print(f"Command: {{' '.join(cmd)}}")
    print("=" * 60)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error: {{e}}")

if __name__ == "__main__":
    main()
'''
        
        with open('auto_launch.py', 'w') as f:
            f.write(script_content)
        
        os.chmod('auto_launch.py', 0o755)
        print("✅ Created auto_launch.py")
    
    def launch(self):
        """Launch WanGP with optimal settings"""
        cmd = ['python', 'wgp.py']
        cmd.extend([
            self.optimal_settings['model'],
            self.optimal_settings['profile'],
            self.optimal_settings['attention']
        ])
        cmd.extend(self.optimal_settings['extra_flags'])
        
        print("🚀 Launching WanGP...")
        print(f"Command: {' '.join(cmd)}")
        print("=" * 60)
        print("📝 Notes:")
        print("• First launch will download models (10-20 minutes)")
        print("• Web interface will be available at the URLs shown")
        print("• Use Ctrl+C to stop")
        print("=" * 60)
        
        try:
            subprocess.run(cmd, check=True)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down WanGP...")
        except Exception as e:
            print(f"❌ Launch failed: {e}")
            print("\n🔧 Troubleshooting:")
            print("1. Check GPU memory availability")
            print("2. Try smaller model: python wgp.py --t2v-1-3B --fp16")
            print("3. Check the logs above for specific errors")

def main():
    """Main function"""
    launcher = WanGPCloudLauncher()
    
    # Print system info
    launcher.print_system_info()
    
    # Setup environment
    launcher.setup_environment()
    
    # Install dependencies if needed
    if '--install-deps' in sys.argv:
        launcher.install_dependencies()
    
    # Create launch script
    launcher.create_launch_script()
    
    # Launch if requested
    if '--launch' in sys.argv:
        launcher.launch()
    else:
        print("\n🎯 Ready to launch!")
        print("Options:")
        print("  python cloud_launcher.py --launch           # Launch now")
        print("  python cloud_launcher.py --install-deps     # Install dependencies")
        print("  python auto_launch.py                       # Use generated launcher")

if __name__ == "__main__":
    main()