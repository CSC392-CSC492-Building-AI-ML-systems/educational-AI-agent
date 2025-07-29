import os
import shutil
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, BitsAndBytesConfig
import runpod

# Set environment variables to use network storage
os.environ['HF_HOME'] = '/runpod-volume/hf_cache'
os.environ['TRANSFORMERS_CACHE'] = '/runpod-volume/hf_cache'
os.environ['HF_HUB_CACHE'] = '/runpod-volume/hf_cache'

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"
NETWORK_MODEL_PATH = "/runpod-volume/autodocs_model_0"
HF_CACHE_DIR = "/runpod-volume/hf_cache"

def check_model_files_exist():
    """Check if all required model files exist in network storage"""
    if not os.path.exists(NETWORK_MODEL_PATH):
        return False

    model_files = os.listdir(NETWORK_MODEL_PATH)
    if not model_files:
        return False

    required_files = [
        "config.json",
        "tokenizer_config.json",
        "tokenizer.json"
    ]

    has_weights = (
        "model.safetensors" in model_files or
        "model.safetensors.index.json" in model_files or
        any(f.endswith(".bin") for f in model_files)
    )

    for file in required_files:
        if not os.path.exists(os.path.join(NETWORK_MODEL_PATH, file)):
            return False

    return has_weights

def clean_and_setup_network_storage():
    """Prepare network volume"""
    if os.path.exists(NETWORK_MODEL_PATH):
        shutil.rmtree(NETWORK_MODEL_PATH)
    if os.path.exists(HF_CACHE_DIR):
        shutil.rmtree(HF_CACHE_DIR)
    os.makedirs(NETWORK_MODEL_PATH, exist_ok=True)
    os.makedirs(HF_CACHE_DIR, exist_ok=True)

# Load model from network storage if exists, else download and save
if check_model_files_exist():
    print("Loading model from network storage...")
    tokenizer = AutoTokenizer.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        NETWORK_MODEL_PATH,
        trust_remote_code=True,
        quantization_config=BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_enable_fp32_cpu_offload=True
        ),
        device_map="auto"
    )
else:
    print("Model not found on network storage. Downloading...")
    clean_and_setup_network_storage()

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        cache_dir=HF_CACHE_DIR,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        cache_dir=HF_CACHE_DIR,
        trust_remote_code=True,
        quantization_config=BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_enable_fp32_cpu_offload=True
        ),
        device_map="auto"
    )

    print("Saving model to network storage...")
    tokenizer.save_pretrained(NETWORK_MODEL_PATH)
    model.save_pretrained(NETWORK_MODEL_PATH)
    print("Saved successfully.")

# Create inference pipeline
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer)

def handler(job):
    job_input = job.get("input", {})
    prompt = job_input.get("prompt", "")
    max_new_tokens = job_input.get("max_new_tokens", 128)
    temperature = job_input.get("temperature", 0.7)

    if not prompt:
        return {"error": "No prompt provided."}

    try:
        output = pipe(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
        return {"output": output[0]["generated_text"]}
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

runpod.serverless.start({"handler": handler})
