# Use a specific PyTorch image for reproducibility
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel-ubuntu22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    wget \
    ffmpeg \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set up the workspace
WORKDIR /workspace

# Copy the entire project into the image
COPY . /workspace/wangp-standalone
WORKDIR /workspace/wangp-standalone

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install xformers for memory-efficient attention, matching the CUDA version
RUN pip install --no-cache-dir xformers==0.0.22 --index-url https://download.pytorch.org/whl/cu121

# Expose the default Gradio port
EXPOSE 7860

# Set environment variables for data paths inside the container
ENV MODEL_CACHE=/workspace/wangp-standalone/assets/models
ENV LORA_CACHE=/workspace/wangp-standalone/assets/loras
ENV OUTPUT_DIR=/workspace/wangp-standalone/assets/outputs

# Create data directories
RUN mkdir -p $MODEL_CACHE $LORA_CACHE $OUTPUT_DIR

# Define the entry point to launch the application
CMD ["python", "-m", "src.app", "--port", "7860"]