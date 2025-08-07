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
    default_prompt = """# Terminal Session Classifier

## Task
Process XML terminal sessions and output:
1. Sequential numbers for each event
2. "0" marks communication boundaries
3. One number per line, no other text

## Rules
- Start numbering at 1 for new communications
- Increment by 1 for each subsequent event
- Output 0 when seeing:
  * New command prompts ($, #)
  * Password prompts
  * Login/logout events
- Never add explanations

## Examples
Input: <system_output>$ </system_output><user_input>ls</user_input>
Output:
1
2
0"""
    
    try:
        with open('system_prompt.txt', 'r') as f:
            content = f.read().strip()
            if not content:
                print("system_prompt.txt is empty, using default")
                return default_prompt
            return content
    except Exception as e:
        print(f"Error loading prompt: {e}, using default")
        return default_prompt

SYSTEM_PROMPT = load_system_prompt()


def format_prompt(user_input):
    """Format with system prompt using clear delimiters"""
    return f"{SYSTEM_PROMPT}\n\n## Current Input\n{user_input}\n\n## Output\n"

# Enhanced output processing
def process_output(raw_text):
    """Extract and validate numerical sequence"""
    numbers = []
    lines = raw_text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Accept only digits and boundary markers
        if line.isdigit() or line == '0':
            numbers.append(line)
        # Special case: Sometimes models add "Output:" before numbers
        elif line.lower().startswith('output:'):
            num_part = line[7:].strip()
            if num_part.isdigit() or num_part == '0':
                numbers.append(num_part)
    
    # Validation: Ensure proper sequence
    if not numbers:
        return "1"  # Fallback
    
    # Convert to integers for validation
    num_sequence = []
    for n in numbers:
        try:
            num_sequence.append(int(n))
        except ValueError:
            continue
    
    # Simple validation - numbers should increment or be 0
    valid_sequence = []
    for i in range(len(num_sequence)):
        if i == 0:
            valid_sequence.append(str(num_sequence[i]))
        else:
            if num_sequence[i] == 0 or num_sequence[i] == num_sequence[i-1] + 1:
                valid_sequence.append(str(num_sequence[i]))
    
    return '\n'.join(valid_sequence) if valid_sequence else "1"

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
        
        return {"output": processed_output}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})