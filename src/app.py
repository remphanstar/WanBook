"""
Main application class for WanGP that handles the model loading,
configuration management, and Gradio server initialization.
"""
import os
import argparse
import logging
from pathlib import Path
import torch
import gradio as gr

from .model_manager import ModelManager
from .gpu_utils import GPUManager
from .interface import create_gradio_interface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WanGPApp:
    """
    Main application class that manages WanGP's lifecycle and components.
    """
    def __init__(self, config=None):
        """
        Initialize the WanGP application with configuration.
        
        Args:
            config (dict, optional): Configuration dictionary with settings for paths,
                                     performance options, and other parameters.
        """
        self.config = config or {}
        
        # Set up default paths
        self.setup_paths()
        
        # Initialize managers
        self.model_manager = ModelManager(
            model_cache_dir=self.config['paths']['model_cache_dir']
        )
        self.gpu_manager = GPUManager()
        
        # Set default performance options if not specified
        if 'performance' not in self.config:
            self.config['performance'] = {
                'precision': 'fp16',
                'enable_xformers': True,
                'cpu_offload': False
            }
            
        # Initialize cuda device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Load GPU info
        if 'gpu_info' not in self.config:
            self.config['gpu_info'] = self.gpu_manager.get_detailed_info()
            
        logger.info(f"Initialized WanGPApp with config: {self.config}")

    def setup_paths(self):
        """Set up default paths for models, LoRAs, and outputs."""
        if 'paths' not in self.config:
            self.config['paths'] = {}
            
        # Use environment variables if available, otherwise use defaults
        default_paths = {
            'model_cache_dir': os.environ.get('MODEL_CACHE', './assets/models'),
            'lora_dir': os.environ.get('LORA_CACHE', './assets/loras'),
            'output_dir': os.environ.get('OUTPUT_DIR', './assets/outputs')
        }
        
        # Set any missing paths to defaults
        for key, default in default_paths.items():
            if key not in self.config['paths']:
                self.config['paths'][key] = default
                
        # Ensure directories exist
        for path in self.config['paths'].values():
            Path(path).mkdir(parents=True, exist_ok=True)

    def generate_video(self, prompt, model_id, num_frames=16, fps=8, **kwargs):
        """
        Generate a video from text prompt using the specified model.
        
        Args:
            prompt (str): Text prompt for video generation
            model_id (str): ID of the model to use
            num_frames (int): Number of frames to generate
            fps (int): Frames per second for the output video
            **kwargs: Additional generation parameters
            
        Returns:
            str: Path to the generated video
        """
        # Load the model
        model = self.model_manager.load_model(model_id)
        
        # TODO: Implement actual generation logic
        # This is a placeholder for the real implementation
        output_path = os.path.join(self.config['paths']['output_dir'], f"generated_video_{model_id}.mp4")
        
        logger.info(f"Generated video at: {output_path}")
        return output_path
    
    def launch(self, share=True, server_port=7860):
        """
        Launch the Gradio interface.
        
        Args:
            share (bool): Whether to create a public link
            server_port (int): Port to run the server on
            
        Returns:
            gr.Blocks: The Gradio interface object
        """
        interface = create_gradio_interface(self, self.config)
        interface.queue().launch(share=share, server_port=server_port)
        return interface

def main():
    """Main entry point for running the application."""
    parser = argparse.ArgumentParser(description="Run WanGP Application")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--share", action="store_true", help="Create a public link")
    args = parser.parse_args()
    
    app = WanGPApp()
    app.launch(share=args.share, server_port=args.port)

if __name__ == "__main__":
    main()