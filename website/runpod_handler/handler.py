import os
import shutil
import re  # NEW: Added for better output processing
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, TextStreamer, torch
import runpod

# NEW: Better disk space monitoring
def log_disk_usage():
    total, used, free = shutil.disk_usage("/")
    print(f"Disk - Total: {total//1024**3}GB, Used: {used//1024**3}GB, Free: {free//1024**3}GB")

os.system("df -h")  # Display disk space information
log_disk_usage()  # NEW: Added detailed disk logging

# NOTE: THE HUGGINGFACE REPO CAN'T CONTAIN THE GGUF FILE, SO WE USE THE NO_GGUF VERSION!!!
MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"  # cmdkp/autodocs_model_0


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

# Load system prompt at startup
SYSTEM_PROMPT = load_system_prompt()

def format_prompt(user_input):
    """Format with system prompt using clear delimiters"""
    return f"{SYSTEM_PROMPT}\n\n## Current Input\n{user_input}\n\n## Output\n"


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

# Load model and tokenizer
try:
    print("Starting model loading process...")
    model, tokenizer = load_model()

    # Create inference pipeline
    print("Creating inference pipeline...")
    pipe = TextGenerationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
    print("Pipeline ready!")
    
except Exception as e:
    print(f"Error during model loading: {str(e)}")
    print("Final disk space check:")
    check_disk_space()
    raise

def handler(job):
    """Handle inference requests with system prompt support"""
    job_input = job.get("input", {})
    prompt = job_input.get("prompt", "")
    max_new_tokens = job_input.get("max_new_tokens", 2048)  # Reduced default
    temperature = job_input.get("temperature", 0.1)  # Lower temperature for more focused output
    do_sample = job_input.get("do_sample", True)
    
    # Optional: Allow custom system prompt per request
    custom_system_prompt = job_input.get("system_prompt", None)
    use_system_prompt = job_input.get("use_system_prompt", True)
    use_simple_format = job_input.get("use_simple_format", False)  # New option

    if not prompt:
        return {"error": "No prompt provided."}

    try:
        # Format prompt with system prompt if enabled
        if use_system_prompt:
            system_to_use = custom_system_prompt if custom_system_prompt else SYSTEM_PROMPT
            if use_simple_format:
                formatted_prompt = format_prompt_simple(prompt, system_to_use)
            else:
                formatted_prompt = format_prompt_with_system(prompt, system_to_use)
        else:
            formatted_prompt = prompt

        # Add generation parameters to encourage concise output

        generation_params = {
            "formatted_prompt": formatted_prompt,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "do_sample": do_sample,
            "pad_token_id": tokenizer.eos_token_id,
            # new params
            "repetition_penalty": 1.1,  # Reduce repetition
            "top_p": 0.9,  # Nucleus sampling
            "top_k": 40,   # Top-k sampling
            "num_beams": 2,        # Added beam search
            "early_stopping": True  # Stop when logical 
        }
        # Format prompt
        formatted_prompt = format_prompt(user_prompt)
        
        output = pipe(
            formatted_prompt,
            streamer=streamer,
            return_full_text=False,
            **generation_params
        )
        
        # Process output (NEW: uses enhanced processing)
        raw_output = output[0]["generated_text"]
        processed_output = process_output(raw_output)
        
        return {"output": processed_output}
    
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})