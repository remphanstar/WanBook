"""
GPU detection and optimization utilities for WanGP.
This module provides functions for detecting available GPUs, measuring memory,
and suggesting optimal settings for different hardware configurations.
"""
import os
import logging
import torch
import psutil
import GPUtil

logger = logging.getLogger(__name__)

class GPUManager:
    """Handles GPU detection, memory management, and optimization."""
    
    def __init__(self):
        """Initialize the GPU manager."""
        self.cuda_available = torch.cuda.is_available()
        self.model_requirements = {
            'wan21_t2v_1.3b': {'min_vram_gb': 6, 'recommended_vram_gb': 8},
            'wan21_t2v_3.5b': {'min_vram_gb': 8, 'recommended_vram_gb': 12},
            'wan21_t2v_14b': {'min_vram_gb': 10, 'recommended_vram_gb': 16},
            'hunyuanvideo': {'min_vram_gb': 16, 'recommended_vram_gb': 24}
        }
    
    def get_detailed_info(self):
        """
        Get detailed information about the GPU and system memory.
        
        Returns:
            dict: Dictionary containing GPU and system information
        """
        info = {
            'cuda_available': self.cuda_available,
            'system_ram_gb': round(psutil.virtual_memory().total / (1024**3), 2)
        }
        
        if self.cuda_available:
            # Get GPU info using PyTorch
            device_count = torch.cuda.device_count()
            info['device_count'] = device_count
            info['device_name'] = torch.cuda.get_device_name(0)
            info['vram_total_gb'] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
            
            try:
                # Get more detailed GPU info using GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # Use the first GPU if multiple are available
                    info['vram_used_gb'] = round(gpu.memoryUsed / 1024, 2)
                    info['vram_free_gb'] = round(gpu.memoryFree / 1024, 2)
                    info['gpu_load'] = round(gpu.load * 100, 1)
                    info['gpu_temperature'] = gpu.temperature
            except Exception as e:
                logger.warning(f"Could not get detailed GPU info via GPUtil: {e}")
        else:
            info['device_count'] = 0
            info['device_name'] = "No GPU detected"
            info['vram_total_gb'] = 0
            info['vram_used_gb'] = 0
            info['vram_free_gb'] = 0
        
        logger.info(f"GPU Info: {info}")
        return info
    
    def get_model_recommendations(self, available_vram_gb):
        """
        Get model recommendations based on available VRAM.
        
        Args:
            available_vram_gb (float): Available VRAM in gigabytes
            
        Returns:
            dict: Dictionary with recommended models by category
        """
        recommendations = {
            'optimal': [],
            'compatible': [],
            'low_memory': []
        }
        
        for model_id, req in self.model_requirements.items():
            if available_vram_gb >= req['recommended_vram_gb']:
                recommendations['optimal'].append(model_id)
            elif available_vram_gb >= req['min_vram_gb']:
                recommendations['compatible'].append(model_id)
            elif available_vram_gb >= req['min_vram_gb'] * 0.8:  # With memory optimizations
                recommendations['low_memory'].append(model_id)
        
        logger.info(f"Model recommendations for {available_vram_gb}GB VRAM: {recommendations}")
        return recommendations
    
    def optimize_for_vram(self, available_vram_gb, model_id):
        """
        Get optimal settings for a model based on available VRAM.
        
        Args:
            available_vram_gb (float): Available VRAM in gigabytes
            model_id (str): ID of the model to optimize for
            
        Returns:
            dict: Dictionary with optimized settings
        """
        settings = {
            'precision': 'fp16',
            'enable_xformers': True,
            'cpu_offload': False,
            'vae_slicing': False,
            'enable_vae_tiling': False,
            'sequential_offload': False,
            'recommended_batch_size': 1
        }
        
        # Get model requirements
        req = self.model_requirements.get(model_id, {'min_vram_gb': 8, 'recommended_vram_gb': 16})
        
        # Apply optimizations based on available VRAM
        if available_vram_gb < req['min_vram_gb']:
            settings['precision'] = 'int8'
            settings['cpu_offload'] = True
            settings['vae_slicing'] = True
            settings['enable_vae_tiling'] = True
            settings['sequential_offload'] = True
        elif available_vram_gb < req['recommended_vram_gb']:
            settings['vae_slicing'] = True
        
        # Set batch size
        if available_vram_gb >= req['recommended_vram_gb'] * 1.5:
            settings['recommended_batch_size'] = 2
        
        logger.info(f"Optimized settings for {model_id} on {available_vram_gb}GB VRAM: {settings}")
        return settings