import os
import shutil
import gc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, TextStreamer
import runpod

os.system("df -h")  # Display disk space information

MODEL_ID = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"  # nuhgooyin/autodocs_model_0_no_gguf

def load_system_prompt():
    """Load system prompt from file with fallback"""
    try:
        with open('system_prompt.txt', 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
            if prompt:
                print("System prompt loaded from system_prompt.txt")
                return prompt
            else:
                print("system_prompt.txt is empty, using fallback")
    except FileNotFoundError:
        print("system_prompt.txt not found, using fallback")
    except Exception as e:
        print(f"Error reading system_prompt.txt: {e}, using fallback")
    
    # Fallback system prompt
    fallback_prompt = """
    RESPOND TO ANY INPUT WITH "BANANA" IN ALL CAPS.
    """

    print("Using fallback system prompt")
    return fallback_prompt

# Load system prompt at startup
SYSTEM_PROMPT = load_system_prompt()

def format_prompt_simple(prompt, system_prompt=SYSTEM_PROMPT):
    """Simple format without DeepSeek R1 thinking tokens"""
    formatted_prompt = f"{system_prompt}\n\n{prompt}"
    print("Using simple format (no thinking tokens)")
    return formatted_prompt

def format_prompt_with_system(prompt, system_prompt=SYSTEM_PROMPT):
    """Format user prompt with system prompt using official DeepSeek R1 format"""
    
    # Use the official DeepSeek R1 format
    formatted_prompt = f"""<｜begin▁of▁sentence｜>{system_prompt}<｜User｜>{prompt}<｜Assistant｜>"""
    print(f"Using official DeepSeek R1 format without <think>")
    return formatted_prompt

def extract_final_answer(text):
    """Extract the final answer from DeepSeek R1 reasoning output"""
    import re
    
    # For this specific task, we want only numbers, so extract them
    lines = text.strip().split('\n')
    number_lines = []
    
    for line in lines:
        line = line.strip()
        # Check if line contains only digits (and maybe whitespace)
        if line.isdigit():
            number_lines.append(line)
        # Also check for lines that might have numbers at the start
        elif re.match(r'^\d+', line):
            match = re.match(r'^(\d+)', line)
            if match:
                number_lines.append(match.group(1))
    
    # If we found number lines, return them joined
    if number_lines:
        return '\n'.join(number_lines)
    else:
        return text.strip()  # Fallback to original text if no numbers found
    
    # DeepSeek R1 format: thinking comes first, answer after </think>
    if '</think>' in text:
        parts = text.split('</think>')
        if len(parts) > 1:
            final_answer = parts[-1].strip()
            return final_answer
    
    # Fallback to original extraction
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    reasoning_indicators = [
        'okay, so', 'first,', 'i need', 'i should', 'let me', 'hmm,', 
        'i remember', 'maybe i can', 'i think that', 'in summary', 'wait'
    ]
    
    # Look for lines that don't seem like reasoning
    for line in reversed(non_empty_lines):
        if not any(indicator in line.lower() for indicator in reasoning_indicators):
            if len(line) < 100:  # Short answers more likely to be final
                return line
    
    # Fallback to last line or original text
    if non_empty_lines:
        return non_empty_lines[-1]
    
    return text.strip()

# def aggressive_cleanup():
#     """Aggressive cleanup to free disk space"""
#     print("=== Performing Aggressive Cleanup ===")
    
#     # Clear Python cache
#     os.system("find / -name '*.pyc' -delete 2>/dev/null")
#     os.system("find / -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null")
    
#     # Clear pip cache
#     os.system("pip cache purge")
    
#     # Clear apt cache (if available)
#     os.system("apt-get clean 2>/dev/null")
    
#     # Clear tmp directories
#     for tmp_dir in ["/tmp", "/var/tmp"]:
#         if os.path.exists(tmp_dir):
#             try:
#                 shutil.rmtree(tmp_dir)
#                 os.makedirs(tmp_dir, exist_ok=True)
#                 print(f"Cleared {tmp_dir}")
#             except:
#                 pass
    
#     # Force garbage collection
#     gc.collect()
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
#         torch.cuda.synchronize()
    
#     print("=== Cleanup Complete ===")
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
    """Load model and tokenizer with 40GB network storage"""
    check_disk_space()
    verify_cache_setup()
    
    print(f"Loading model: {MODEL_ID}")
    
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        use_fast=True,
        cache_dir="/runpod-volume"
    )
    
    # Load model - should fit easily in 40GB network storage
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        device_map="auto",
        torch_dtype="auto",
        cache_dir="/runpod-volume"
    )
    
    print("Model loaded successfully!")
    
    # Display loaded system prompt
    print("=== System Prompt Configuration ===")
    print(f"System prompt length: {len(SYSTEM_PROMPT)} characters")
    print("===================================")
    
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
        return_full_text=False,
        clean_up_tokenization_spaces=True
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
    max_new_tokens = job_input.get("max_new_tokens", 2048)  # Restored to original
    temperature = job_input.get("temperature", 0.1)  # Lower temperature for more focused output
    do_sample = job_input.get("do_sample", True)
    
    # Optional: Allow custom system prompt per request
    custom_system_prompt = job_input.get("system_prompt", None)
    use_system_prompt = job_input.get("use_system_prompt", True)
    use_simple_format = job_input.get("use_simple_format", False)

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

        # Generation parameters 
        generation_params = {
            "formatted_prompt": formatted_prompt,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "do_sample": do_sample,
            "pad_token_id": tokenizer.eos_token_id,
            "repetition_penalty": 1.1,
            "top_p": 0.9,
            "top_k": 50,
        }

        streamer = TextStreamer(tokenizer, skip_prompt=False, skip_special_tokens=True)
        
        output = pipe(
            formatted_prompt,
            streamer=streamer,
            **generation_params
        )
        
        raw_output = output[0]["generated_text"]
        print(f"Raw output: {raw_output}")
        
        # Extract final answer from reasoning output
        final_answer = extract_final_answer(raw_output)
        
        return {"output": final_answer}
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})