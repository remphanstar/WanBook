"""
Core video generation logic for WanGP.
Implements text-to-video, image-to-video, and other generation methods.
"""
import os
import logging
import torch
import numpy as np
from pathlib import Path
import time
import uuid

logger = logging.getLogger(__name__)

class VideoGenerator:
    """Handles all video generation tasks."""
    
    def __init__(self, model_manager, config=None):
        """
        Initialize the video generator.
        
        Args:
            model_manager (ModelManager): Instance of ModelManager for loading models
            config (dict, optional): Configuration dictionary
        """
        self.model_manager = model_manager
        self.config = config or {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Set default output directory
        self.output_dir = Path(self.config.get('paths', {}).get(
            'output_dir', os.environ.get('OUTPUT_DIR', './assets/outputs')
        ))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized VideoGenerator with output directory: {self.output_dir}")
    
    def generate_from_text(self, prompt, model_id, num_frames=16, fps=8, guidance_scale=7.5, 
                           num_inference_steps=25, seed=None, width=512, height=512, 
                           negative_prompt=None, callback=None):
        """
        Generate a video from a text prompt.
        
        Args:
            prompt (str): Text prompt for generation
            model_id (str): ID of the model to use
            num_frames (int): Number of frames to generate
            fps (int): Frames per second for output video
            guidance_scale (float): Guidance scale for generation
            num_inference_steps (int): Number of inference steps
            seed (int, optional): Random seed for reproducibility
            width (int): Width of generated frames
            height (int): Height of generated frames
            negative_prompt (str, optional): Negative prompt for generation
            callback (callable, optional): Progress callback function
            
        Returns:
            dict: Dictionary with output paths and generation info
        """
        start_time = time.time()
        
        # Set seed for reproducibility
        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)
        else:
            seed = torch.randint