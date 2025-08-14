import os
import shutil
import re 
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, TextStreamer
import runpod


def log_disk_usage():
    total, used, free = shutil.disk_usage("/")
    print(f"Disk - Total: {total//1024**3}GB, Used: {used//1024**3}GB, Free: {free//1024**3}GB")

os.system("df -h")  # Display disk space information
log_disk_usage()  

MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

def load_system_prompt():
    """Load and validate system prompt"""
    with open('system_prompt.txt', 'r') as f:
        content = f.read().strip()
    return content

SYSTEM_PROMPT = load_system_prompt()

def format_prompt(user_input):
    """Format with system prompt using clear delimiters"""
    return f"{SYSTEM_PROMPT}\n\n## Current Input\n{user_input}\n\n## Output\n"

# Enhanced output processing
def process_output(raw_text):
    """Extract and validate numerical sequence"""
    pass

# NEW: Optimized model loading
def load_model():
    """Load model with better error handling"""
    try:
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID,
            trust_remote_code=True
        )
        
        print("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto",
            torch_dtype="auto",
            low_cpu_mem_usage=True
        )
        
        return model, tokenizer
    except Exception as e:
        log_disk_usage()
        raise RuntimeError(f"Model loading failed: {str(e)}")

# Load model
try:
    model, tokenizer = load_model()
    pipe = TextGenerationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
except Exception as e:
    print(f"Initialization failed: {e}")
    exit(1)

def handler(job):
    """Handle inference requests"""
    try:
        job_input = job.get("input", {})
        user_prompt = job_input.get("prompt", "")
        
        if not user_prompt:
            return {"error": "Empty input"}
        
        # Generation parameters optimized for numbering task
        generation_params = {
            "max_new_tokens": 100,  # Reduced since we only need numbers
            "temperature": 0.3,     # Balanced between creativity and determinism
            "top_p": 0.9,
            "top_k": 40,
            "repetition_penalty": 1.2,
            "do_sample": True,
            "num_beams": 2,        # NEW: Added beam search
            "early_stopping": True  # NEW: Stop when logical sequence completes
        }
        
        # Format prompt (NEW: uses simplified formatting)
        formatted_prompt = format_prompt(user_prompt)
        
        # Generate output
        output = pipe(
            formatted_prompt,
            return_full_text=False,
            **generation_params
        )
        
        # Process output
        raw_output = output[0]["generated_text"]
        processed_output = process_output(raw_output)
        
        return {"output": raw_output}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})