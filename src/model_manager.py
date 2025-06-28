"""
Model manager for WanGP that handles downloading, loading, and caching models.
"""
import os
import logging
import yaml
import torch
from pathlib import Path
from huggingface_hub import snapshot_download
from collections import OrderedDict

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manages downloading, loading, and caching of models.
    Implements an LRU cache to efficiently manage models in GPU memory.
    """
    
    def __init__(self, model_cache_dir='./assets/models', config_path='./configs/models.yaml', 
                 max_models_in_memory=2):
        """
        Initialize the model manager.
        
        Args:
            model_cache_dir (str): Directory to store downloaded models
            config_path (str): Path to the model registry YAML file
            max_models_in_memory (int): Maximum number of models to keep in memory
        """
        self.model_cache_dir = Path(model_cache_dir)
        self.model_cache_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = config_path
        self.max_models_in_memory = max_models_in_memory
        
        # LRU cache for loaded models
        self.model_cache = OrderedDict()
        
        # Load model catalog
        self.model_catalog = self.load_model_catalog()
        
        logger.info(f"Initialized ModelManager with cache directory: {model_cache_dir}")
        logger.info(f"Found {len(self.model_catalog)} models in catalog")
    
    def load_model_catalog(self):
        """
        Load the model catalog from the YAML config file.
        If file doesn't exist, return a default catalog.
        
        Returns:
            dict: Model catalog with model IDs as keys
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    catalog = yaml.safe_load(f)
                    return catalog.get('models', {})
            else:
                # Return default catalog if config file doesn't exist
                logger.warning(f"Model config not found at {self.config_path}, using default catalog")
                return self.get_default_catalog()
        except Exception as e:
            logger.error(f"Error loading model catalog: {e}")
            return self.get_default_catalog()
    
    def get_default_catalog(self):
        """
        Return a default catalog of WanGP models.
        
        Returns:
            dict: Default model catalog
        """
        return {
            'wan21_t2v_1.3b': {
                'name': 'WanGP T2V 1.3B',
                'repo_id': 'wangp/wangp-t2v-1.3b',
                'type': 't2v',
                'size': '2.1 GB',
                'min_vram_gb': 6,
                'default_steps': 20
            },
            'wan21_t2v_14b': {
                'name': 'WanGP T2V 14B',
                'repo_id': 'wangp/wangp-t2v-14b',
                'type': 't2v',
                'size': '14.8 GB',
                'min_vram_gb': 10,
                'default_steps': 25
            },
            'hunyuanvideo': {
                'name': 'HunyuanVideo',
                'repo_id': 'wangp/hunyuanvideo',
                'type': 't2v',
                'size': '22.5 GB',
                'min_vram_gb': 16,
                'default_steps': 30
            }
        }
    
    def get_model_catalog(self):
        """
        Return the current model catalog.
        
        Returns:
            dict: Model catalog with model IDs as keys
        """
        return self.model_catalog
    
    def download_model(self, model_id):
        """
        Download a model from HuggingFace Hub.
        
        Args:
            model_id (str): ID of the model to download
            
        Returns:
            str: Path to the downloaded model
        """
        if model_id not in self.model_catalog:
            raise ValueError(f"Model ID '{model_id}' not found in catalog")
        
        model_info = self.model_catalog[model_id]
        repo_id = model_info['repo_id']
        
        # Create model-specific directory
        model_dir = self.model_cache_dir / model_id
        
        if model_dir.exists():
            logger.info(f"Model {model_id} already exists at {model_dir}")
            return str(model_dir)
        
        logger.info(f"Downloading model {model_id} from {repo_id}")
        
        try:
            local_dir = snapshot_download(
                repo_id=repo_id,
                local_dir=str(model_dir),
                local_dir_use_symlinks=False
            )
            logger.info(f"Downloaded model {model_id} to {local_dir}")
            return local_dir
        except Exception as e:
            logger.error(f"Error downloading model {model_id}: {e}")
            raise
    
    def load_model(self, model_id):
        """
        Load a model into memory, downloading it first if necessary.
        Implements LRU caching to manage memory efficiently.
        
        Args:
            model_id (str): ID of the model to load
            
        Returns:
            object: The loaded model
        """
        # Check if model is already in cache
        if model_id in self.model_cache:
            # Move to end of OrderedDict to mark as recently used
            model = self.model_cache.pop(model_id)
            self.model_cache[model_id] = model
            logger.info(f"Using cached model {model_id}")
            return model
        
        # Ensure model is downloaded
        model_path = self.download_model(model_id)
        
        # TODO: Implement actual model loading logic
        # This is a placeholder for the real implementation
        logger.info(f"Loading model {model_id} from {model_path}")
        model = {"id": model_id, "path": model_path}  # Placeholder
        
        # Add to cache, removing least recently used if needed
        if len(self.model_cache) >= self.max_models_in_memory:
            # Remove the first item (least recently used)
            lru_model_id, _ = self.model_cache.popitem(last=False)
            logger.info(f"Removing least recently used model {lru_model_id} from cache")
            # Free memory by explicitly removing references
            torch.cuda.empty_cache()
        
        # Add new model to cache
        self.model_cache[model_id] = model
        
        return model


class ModelDownloader:
    """Helper class for downloading models, especially through UI interfaces."""
    
    def __init__(self, model_cache_dir='./assets/models'):
        """
        Initialize the model downloader.
        
        Args:
            model_cache_dir (str): Directory to store downloaded models
        """
        self.model_manager = ModelManager(model_cache_dir=model_cache_dir)
    
    def download_model(self, model_id, model_info=None):
        """
        Download a model with progress updates.
        
        Args:
            model_id (str): ID of the model to download
            model_info (dict, optional): Model information dictionary
            
        Returns:
            str: Path to the downloaded model
        """
        try:
            # Use model_info if provided, otherwise get from catalog
            if model_info is None:
                model_catalog = self.model_manager.get_model_catalog()
                if model_id not in model_catalog:
                    raise ValueError(f"Model ID '{model_id}' not found in catalog")
                model_info = model_catalog[model_id]
            
            # Download the model
            return self.model_manager.download_model(model_id)
        except Exception as e:
            logger.error(f"Error downloading model {model_id}: {e}")
            raise