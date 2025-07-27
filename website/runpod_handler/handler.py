import os
import shutil
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import runpod

# Set environment variables to force all HuggingFace operations to use network storage
os.environ['HF_HOME'] = '/runpod-volume/hf_cache'
os.environ['TRANSFORMERS_CACHE'] = '/runpod-volume/hf_cache'
os.environ['HF_HUB_CACHE'] = '/runpod-volume/hf_cache'

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"
NETWORK_MODEL_PATH = "/runpod-volume/autodocs_model_0"

def check_model_files_exist():
    """Check if all required model files exist in network storage"""
    if not os.path.exists(NETWORK_MODEL_PATH):
        print("Model directory does not exist")
        return False
    
    try:
        model_files = os.listdir(NETWORK_MODEL_PATH)
        print(f"Files in model directory: {model_files}")
    except Exception as e:
        print(f"Error reading model directory: {e}")
        return False
    
    if not model_files:
        print("Model directory is empty")
        return False
    
    required_files = [
        "config.json",
        "tokenizer_config.json", 
        "tokenizer.json"
    ]
    
    # Check for model weights
    has_safetensors_index = "model.safetensors.index.json" in model_files
    has_sharded_safetensors = any(f.startswith("model-") and f.endswith(".safetensors") for f in model_files)
    has_single_safetensors = "model.safetensors" in model_files
    has_pytorch = any(f.endswith('.bin') for f in model_files)
    
    print(f"Has safetensors index: {has_safetensors_index}")
    print(f"Has sharded safetensors: {has_sharded_safetensors}")
    print(f"Has single safetensors: {has_single_safetensors}")
    print(f"Has pytorch: {has_pytorch}")
    
    # For sharded models, we need both the index file and shard files
    if has_safetensors_index and has_sharded_safetensors:
        model_format_ok = True
    elif has_single_safetensors or has_pytorch:
        model_format_ok = True
    else:
        model_format_ok = False
    
    if not model_format_ok:
        print("No valid model weight files found")
        return False
        
    # Check for required config files
    missing_files = []
    for file in required_files:
        file_path = os.path.join(NETWORK_MODEL_PATH, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required files: {missing_files}")
        return False
    
    print("All required model files found")
    return True

def clean_and_setup_network_storage():
    """Clean network storage and ensure directories exist"""
    # Remove existing model directory if it exists
    if os.path.exists(NETWORK_MODEL_PATH):
        print(f"Cleaning existing model directory: {NETWORK_MODEL_PATH}")
        shutil.rmtree(NETWORK_MODEL_PATH)
    
    # Remove HuggingFace cache if it exists
    hf_cache_dir = "/runpod-volume/hf_cache"
    if os.path.exists(hf_cache_dir):
        print(f"Cleaning HuggingFace cache: {hf_cache_dir}")
        shutil.rmtree(hf_cache_dir)
    
    # Create directories
    os.makedirs(NETWORK_MODEL_PATH, exist_ok=True)
    os.makedirs(hf_cache_dir, exist_ok=True)
    print("Network storage cleaned and prepared")

# Check if model already exists and is complete on network storage
if check_model_files_exist():
    print("Model found on network storage. Loading existing model...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
        print("Model loaded successfully from network storage")
    except Exception as e:
        print(f"Error loading model from network storage: {e}")
        print("Falling back to download...")
        # Clean and prepare network storage
        clean_and_setup_network_storage()
        
        print("Downloading model directly to network storage...")
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID, 
            cache_dir="/runpod-volume/hf_cache",
            trust_remote_code=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, 
            cache_dir="/runpod-volume/hf_cache",
            trust_remote_code=True
        )
        
        print("Saving model to network storage for future use...")
        tokenizer.save_pretrained(NETWORK_MODEL_PATH)
        model.save_pretrained(NETWORK_MODEL_PATH)
        print("Model saved successfully to network storage")
else:
    print("Model not found on network storage. Downloading...")
    # Clean and prepare network storage
    clean_and_setup_network_storage()
    
    print("Downloading model directly to network storage...")
    # Download directly to network storage using cache_dir
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, 
        cache_dir="/runpod-volume/hf_cache",
        trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, 
        cache_dir="/runpod-volume/hf_cache",
        trust_remote_code=True
    )
    
    print("Saving model to network storage for future use...")
    # Save in standard format for faster loading next time
    tokenizer.save_pretrained(NETWORK_MODEL_PATH)
    model.save_pretrained(NETWORK_MODEL_PATH)
    print("Model saved successfully to network storage")

print("Creating inference pipeline...")
# Create pipeline - this loads model weights into GPU memory
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer, device=0)
print("Pipeline ready for inference")

def handler(event):
    # Inference happens on worker GPU
    input_data = event.get("input", {})
    prompt = input_data.get("prompt", "")
    max_new_tokens = input_data.get("max_new_tokens", 128)
    temperature = input_data.get("temperature", 0.7)

    if not prompt:
        return {"error": "No prompt provided."}

    output = pipe(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
    return {"output": output[0]["generated_text"]}

runpod.serverless.start({"handler": handler})
