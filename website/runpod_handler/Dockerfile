# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY handler.py .
COPY system_prompt.txt .

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Set environment variables for Hugging Face caching
# These will direct all HF downloads to the network storage
ENV HF_HOME=/runpod-volume/huggingface
ENV TRANSFORMERS_CACHE=/runpod-volume/huggingface
ENV HF_HUB_CACHE=/runpod-volume/huggingface/hub
ENV HF_DATASETS_CACHE=/runpod-volume/huggingface/datasets

# Critical: Force temporary files to network storage too
ENV TMPDIR=/runpod-volume/tmp
ENV TEMP=/runpod-volume/tmp
ENV TMP=/runpod-volume/tmp

# Additional environment variables for optimization
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1

# Debug: Show disk usage during build (this will show build-time disk usage)
RUN df -h

# Create cache directories and symbolic links to force all cache to network storage
RUN mkdir -p /runpod-volume/huggingface/hub && \
    mkdir -p /runpod-volume/tmp

# Run the handler
CMD ["python", "handler.py"]