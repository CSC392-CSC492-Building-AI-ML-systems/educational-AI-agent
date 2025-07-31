import os
import shutil
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import runpod

os.system("df -h")  # Display disk space information

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"

def check_disk_space():
    """Check available disk space in key locations"""
    locations = ["/", "/runpod-volume", "/tmp"]
    
    print("=== Disk Space Check ===")
    for location in locations:
        if os.path.exists(location):
            total, used, free = shutil.disk_usage(location)
            print(f"{location:15} - Total: {total//1024**3:3d}GB, Used: {used//1024**3:3d}GB, Free: {free//1024**3:3d}GB")
        else:
            print(f"{location:15} - Does not exist")
    print("========================")

def verify_cache_setup():
    """Verify that cache directories are properly set up"""
    print("=== Cache Setup Verification ===")
    cache_vars = ['HF_HOME', 'TRANSFORMERS_CACHE', 'HF_HUB_CACHE', 'HF_DATASETS_CACHE']
    
    for var in cache_vars:
        value = os.environ.get(var, 'Not set')
        print(f"{var:20}: {value}")
        if value != 'Not set' and not os.path.exists(value):
            print(f"  Warning: Directory {value} does not exist")
            os.makedirs(value, exist_ok=True)
            print(f"  Created directory: {value}")
    print("=================================")

def load_model():
    """Load model and tokenizer"""
    check_disk_space()
    verify_cache_setup()
    
    print(f"Loading model: {MODEL_ID}")
    
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        use_fast=True
    )
    
    # Load model
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        device_map="auto",
        torch_dtype="auto"
    )
    
    print("Model loaded successfully!")
    
    # Final disk space check
    print("=== Post-Loading Disk Space ===")
    check_disk_space()
    
    return model, tokenizer

# Load model and tokenizer
try:
    print("Starting model loading process...")
    model, tokenizer = load_model()
    
    # Create inference pipeline
    print("Creating inference pipeline...")
    pipe = TextGenerationPipeline(
        model=model, 
        tokenizer=tokenizer,
        device_map="auto"
    )
    print("Pipeline ready! ✅")
    
except Exception as e:
    print(f"❌ Error during model loading: {str(e)}")
    print("Final disk space check:")
    check_disk_space()
    raise

def handler(job):
    """Handle inference requests"""
    job_input = job.get("input", {})
    prompt = job_input.get("prompt", "")
    max_new_tokens = job_input.get("max_new_tokens", 128)
    temperature = job_input.get("temperature", 0.7)
    do_sample = job_input.get("do_sample", True)

    if not prompt:
        return {"error": "No prompt provided."}

    try:
        output = pipe(
            prompt, 
            max_new_tokens=max_new_tokens, 
            temperature=temperature,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id,
            return_full_text=False
        )
        
        return {"output": output[0]["generated_text"]}
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})