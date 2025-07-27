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
        return False
    
    required_files = [
        "config.json",
        "tokenizer_config.json", 
        "tokenizer.json"
    ]
    
    # Check for model weights (either safetensors or pytorch format)
    model_files = os.listdir(NETWORK_MODEL_PATH)
    has_safetensors = any(f.endswith('.safetensors') for f in model_files)
    has_pytorch = any(f.endswith('.bin') for f in model_files)
    
    if not (has_safetensors or has_pytorch):
        return False
        
    # Check for required config files
    for file in required_files:
        if not os.path.exists(os.path.join(NETWORK_MODEL_PATH, file)):
            return False
    
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
    tokenizer = AutoTokenizer.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
    print("Model loaded successfully from network storage")
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
