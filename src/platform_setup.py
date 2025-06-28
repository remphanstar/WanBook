"""
Platform-specific setup for WanGP.
Handles environment detection and configuration for different platforms
like Google Colab, Vast.ai, local installations, etc.
"""
import os
import sys
import subprocess
import logging
import time
import pkg_resources
import importlib.util
from pathlib import Path

logger = logging.getLogger(__name__)

class PlatformSetup:
    """
    Handles platform-specific setup operations for different environments.
    """
    
    def __init__(self, environment, system_info):
        """
        Initialize the platform setup with environment information.
        
        Args:
            environment (str): The detected environment (e.g., 'colab', 'vast', 'local')
            system_info (dict): Information about the system and GPU
        """
        self.environment = environment
        self.system_info = system_info
        self.required_packages = {
            'base': [
                'torch>=2.1.0', 'torchvision>=0.16.0', 'gradio>=4.11.0', 
                'diffusers>=0.24.0', 'transformers>=4.37.0', 'accelerate>=0.25.0',
                'safetensors', 'einops', 'huggingface-hub', 'PyYAML', 
                'psutil', 'GPUtil', 'tqdm'
            ],
            'video': ['imageio-ffmpeg', 'opencv-python-headless'],
            'optimization': ['bitsandbytes'],
            'notebook': ['ipywidgets']
        }
        
        # Set environment variables for data paths
        if 'MODEL_CACHE' not in os.environ:
            os.environ['MODEL_CACHE'] = str(Path('./assets/models').absolute())
        if 'LORA_CACHE' not in os.environ:
            os.environ['LORA_CACHE'] = str(Path('./assets/loras').absolute())
        if 'OUTPUT_DIR' not in os.environ:
            os.environ['OUTPUT_DIR'] = str(Path('./assets/outputs').absolute())
        
        # Create necessary directories
        for env_var in ['MODEL_CACHE', 'LORA_CACHE', 'OUTPUT_DIR']:
            Path(os.environ[env_var]).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized PlatformSetup for {environment} environment")
    
    def run(self, progress_callback=None):
        """
        Run the platform-specific setup process.
        
        Args:
            progress_callback (callable, optional): Function to report progress
        
        Returns:
            bool: True if setup was successful
        """
        try:
            # Report initial progress
            if progress_callback:
                progress_callback(5, "Starting platform setup")
            
            # Choose the right setup method based on environment
            setup_methods = {
                'colab': self._setup_colab,
                'kaggle': self._setup_kaggle,
                'paperspace': self._setup_paperspace,
                'vast': self._setup_vast,
                'lightning': self._setup_lightning,
                'runpod': self._setup_runpod,
                'docker': self._setup_docker,
                'jupyter': self._setup_jupyter,
                'local': self._setup_local
            }
            
            # Run the appropriate setup method
            setup_method = setup_methods.get(self.environment, self._setup_generic)
            setup_method(progress_callback)
            
            # Install or update required packages
            self._install_required_packages(progress_callback)
            
            # Final setup steps common to all platforms
            self._common_setup_steps(progress_callback)
            
            if progress_callback:
                progress_callback(100, "Setup completed successfully")
            
            logger.info(f"Platform setup for {self.environment} completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during platform setup: {e}")
            if progress_callback:
                progress_callback(0, f"Error: {str(e)}")
            return False
    
    def _setup_colab(self, progress_callback=None):
        """
        Set up for Google Colab environment.
        
        Args:
            progress_callback (callable, optional): Function to report progress
        """
        if progress_callback:
            progress_callback(10, "Setting up Colab environment")
            
        # Configure for Google Drive if available
        drive_mounted = False
        try:
            from google.colab import drive
            if progress_callback:
                progress_callback(20, "Mounting Google Drive")
            drive.mount('/content/drive', force_remount=True)
            drive_mounted = True
            
            # Set persistent storage paths in Drive
            models_dir = Path('/content/drive/MyDrive/wangp/models')
            loras_dir = Path('/content/drive/MyDrive/wangp/loras')
            outputs_dir = Path('/content/drive/MyDrive/wangp/outputs')
            
            models_dir.mkdir(parents=True, exist_ok=True)
            loras_dir.mkdir(parents=True, exist_ok=True)
            outputs_dir.mkdir(parents=True, exist_ok=True)
            
            os.environ['MODEL_CACHE'] = str(models_dir)
            os.environ['LORA_CACHE'] = str(loras_dir)
            os.environ['OUTPUT_DIR'] = str(outputs_dir)
            
            if progress_callback:
                progress_callback(30, "Google Drive mounted and configured")
                
        except ImportError:
            logger.warning("Could not import Google Drive module")
        except Exception as e:
            logger.warning(f"Error mounting Google Drive: {e}")
        
        # Install xformers for Colab
        if self.system_info.get('cuda_available', False):
            if progress_callback:
                progress_callback(40, "Installing xformers")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", 
                    "xformers==0.0.22", "--no-deps", 
                    "--index-url", "https://download.pytorch.org/whl/cu121"
                ], check=True)
            except subprocess.SubprocessError as e:
                logger.warning(f"Error installing xformers: {e}")
        
        if progress_callback:
            progress_callback(50, "Colab environment setup complete")
        
        logger.info(f"Colab setup completed. Drive mounted: {drive_mounted}")
    
    def _setup_vast(self, progress_callback=None):
        """
        Set up for Vast.ai environment.
        
        Args:
            progress_callback (callable, optional): Function to report progress
        """
        if progress_callback:
            progress_callback(10, "Setting up Vast.ai environment")
        
        # Vast.ai specific setup
        # Usually paths are already configured in the Docker container
        
        if progress_callback:
            progress_callback(50, "Vast.ai environment setup complete")
        
        logger.info("Vast.ai setup completed")
    
    def _setup_generic(self, progress_callback=None):
        """
        Generic setup for environments without specific handling.
        
        Args:
            progress_callback (callable, optional): Function to report progress
        """
        if progress_callback:
            progress_callback(10, f"Setting up {self.environment} environment")
        
        if progress_callback:
            progress_callback(50, f"Generic environment setup complete")
        
        logger.info(f"Generic setup completed for {self.environment}")
    
    def _setup_jupyter(self, progress_callback=None):
        """Setup for Jupyter environment."""
        if progress_callback:
            progress_callback(10, "Setting up Jupyter environment")
        
        # No special setup needed for Jupyter
        
        if progress_callback:
            progress_callback(50, "Jupyter environment setup complete")
        
        logger.info("Jupyter setup completed")
    
    def _setup_local(self, progress_callback=None):
        """Setup for local Python environment."""
        if progress_callback:
            progress_callback(10, "Setting up local environment")
        
        # No special setup needed for local environment
        
        if progress_callback:
            progress_callback(50, "Local environment setup complete")
        
        logger.info("Local setup completed")
    
    def _setup_kaggle(self, progress_callback=None):
        """Setup for Kaggle environment."""
        # Implementation similar to Colab
        pass
    
    def _setup_paperspace(self, progress_callback=None):
        """Setup for Paperspace environment."""
        # Paperspace specific implementation
        pass
    
    def _setup_lightning(self, progress_callback=None):
        """Setup for Lightning.ai environment."""
        # Lightning.ai specific implementation
        pass
    
    def _setup_runpod(self, progress_callback=None):
        """Setup for RunPod environment."""
        # RunPod specific implementation
        pass
    
    def _setup_docker(self, progress_callback=None):
        """Setup for Docker environment."""
        # Docker specific implementation
        pass
    
    def _install_required_packages(self, progress_callback=None):
        """
        Install or update required Python packages.
        
        Args:
            progress_callback (callable, optional): Function to report progress
        """
        if progress_callback:
            progress_callback(60, "Checking required packages")
        
        # Get currently installed packages
        installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        
        # Collect packages to install
        to_install = []
        
        # Combine all required packages
        all_requirements = []
        for package_group in self.required_packages.values():
            all_requirements.extend(package_group)
        
        # Check which packages need to be installed or updated
        for req in all_requirements:
            # Parse package name and version constraint
            if '>=' in req:
                pkg_name, version_constraint = req.split('>=')
                pkg_name = pkg_name.strip()
                if pkg_name not in installed_packages:
                    to_install.append(req)
                # We're not checking for updates here to keep it simpler
            else:
                pkg_name = req.strip()
                if pkg_name not in installed_packages:
                    to_install.append(req)
        
        # Install missing packages
        if to_install:
            if progress_callback:
                progress_callback(70, f"Installing {len(to_install)} packages")
            
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade"
                ] + to_install, check=True)
            except subprocess.SubprocessError as e:
                logger.error(f"Error installing packages: {e}")
                if progress_callback:
                    progress_callback(75, f"Some packages failed to install")
        else:
            if progress_callback:
                progress_callback(70, "All required packages already installed")
    
    def _common_setup_steps(self, progress_callback=None):
        """
        Common setup steps for all platforms.
        
        Args:
            progress_callback (callable, optional): Function to report progress
        """
        if progress_callback:
            progress_callback(80, "Running common setup steps")
        
        # Create necessary directories
        for path_name in ['MODEL_CACHE', 'LORA_CACHE', 'OUTPUT_DIR']:
            dir_path = os.environ.get(path_name)
            if dir_path:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create default config files if they don't exist
        configs_dir = Path('./configs')
        configs_dir.mkdir(exist_ok=True)
        
        default_models_yaml = configs_dir / 'models.yaml'
        if not default_models_yaml.exists():
            if progress_callback:
                progress_callback(90, "Creating default model config")
            
            # Create a minimal default models.yaml
            with open(default_models_yaml, 'w') as f:
                f.write("""models:
  wan21_t2v_1.3b:
    name: WanGP T2V 1.3B
    repo_id: wangp/wangp-t2v-1.3b
    type: t2v
    size: 2.1 GB
    min_vram_gb: 6
    default_steps: 20
  wan21_t2v_14b:
    name: WanGP T2V 14B
    repo_id: wangp/wangp-t2v-14b
    type: t2v
    size: 14.8 GB
    min_vram_gb: 10
    default_steps: 25
  hunyuanvideo:
    name: HunyuanVideo
    repo_id: wangp/hunyuanvideo
    type: t2v
    size: 22.5 GB
    min_vram_gb: 16
    default_steps: 30
""")
        
        if progress_callback:
            progress_callback(95, "Common setup steps completed")