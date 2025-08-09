import os
import shutil
import re
import torch  # Required for device detection
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, TextStreamer
import runpod

# --- Disk Monitoring Utilities ---
def log_disk_usage():
    """Log detailed disk space information"""
    total, used, free = shutil.disk_usage("/")
    print(f"Disk - Total: {total//1024**3}GB, Used: {used//1024**3}GB, Free: {free//1024**3}GB")

# Initial disk space log
os.system("df -h")
log_disk_usage()

# --- Model Configuration ---
MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"

# --- System Prompt Handling ---
DEFAULT_SYSTEM_PROMPT = """# Terminal Session Classifier

## Task
Process XML terminal sessions and output sequential numbers:
1. Start at 1 for new communications
2. Increment by 1 for each event
3. Use 0 to mark boundaries

## Rules
- Never include XML tags
- One number per line
- Reset to 1 after boundary markers
- No explanations or extra text

## Example
Input: <system_output>$ </system_output><user_input>ls</user_input>
Output:
1
2
0"""

def load_system_prompt():
    """Load system prompt with fallback to default"""
    try:
        if os.path.exists('system_prompt.txt'):
            with open('system_prompt.txt', 'r') as f:
                content = f.read().strip()
                if content:
                    return content
        return DEFAULT_SYSTEM_PROMPT
    except Exception as e:
        print(f"Prompt loading error: {e}")
        return DEFAULT_SYSTEM_PROMPT

SYSTEM_PROMPT = load_system_prompt()

# --- Prompt Formatting ---
def format_prompt(user_input):
    """Create properly structured prompt"""
    return f"{SYSTEM_PROMPT}\n\n## Input XML\n{user_input}\n\n## Numbered Sequence\n"

# --- Output Processing ---
def validate_sequence(numbers):
    """Ensure proper number sequencing"""
    for i in range(1, len(numbers)):
        if numbers[i] != 0 and numbers[i] != numbers[i-1] + 1:
            return False
    return True

def process_output(raw_text):
    """Extract and validate number sequence"""
    numbers = []
    for line in raw_text.split('\n'):
        line = line.strip()
        if line.isdigit() or line == '0':
            numbers.append(int(line))
    
    # If sequence is invalid, generate simple incrementing sequence
    if not validate_sequence(numbers):
        count = len(re.findall(r'<(user_input|system_output)', job_input.get("prompt", "")))
        numbers = list(range(1, count+1))
    
    return '\n'.join(map(str, numbers))

# --- Model Loading ---
def load_model():
    """Load model with error handling"""
    print("Loading model components...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID,
            trust_remote_code=True
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto",
            torch_dtype="auto" if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True
        )
        return model, tokenizer
    except Exception as e:
        log_disk_usage()
        raise RuntimeError(f"Model loading failed: {str(e)}")

# --- Pipeline Creation ---
def create_pipeline(model, tokenizer):
    """Create pipeline with multiple fallback options"""
    # Try CUDA first if available
    if torch.cuda.is_available():
        try:
            return TextGenerationPipeline(
                model=model,
                tokenizer=tokenizer,
                device=0,
                return_full_text=False
            )
        except Exception as e:
            print(f"CUDA pipeline failed, trying auto: {e}")
    
    # Fallback to automatic device mapping
    try:
        return TextGenerationPipeline(
            model=model,
            tokenizer=tokenizer,
            device_map="auto",
            return_full_text=False
        )
    except Exception as e:
        print(f"Auto mapping failed, trying CPU: {e}")
    
    # Final CPU fallback
    return TextGenerationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=-1,
        return_full_text=False
    )

# --- Initialization ---
try:
    model, tokenizer = load_model()
    pipe = create_pipeline(model, tokenizer)
    print("Pipeline successfully initialized")
except Exception as e:
    print(f"Initialization failed: {e}")
    exit(1)

# --- Handler Function ---
def handler(job):
    """Main request handler"""
    try:
        job_input = job.get("input", {})
        user_prompt = job_input.get("prompt", "")
        
        if not user_prompt:
            return {"error": "Empty input provided"}
        
        # Generation parameters
        gen_params = {
            "max_new_tokens": 50,
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "repetition_penalty": 1.2,
            "do_sample": True,
            "early_stopping": True
        }
        
        # Process input and generate output
        formatted_prompt = format_prompt(user_prompt)
        raw_output = pipe(formatted_prompt, **gen_params)[0]["generated_text"]
        processed_output = process_output(raw_output)
        
        return {"output": processed_output}
    
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

# --- Runpod Setup ---
if __name__ == "__main__":
    print("Starting Runpod serverless handler")
    runpod.serverless.start({"handler": handler})