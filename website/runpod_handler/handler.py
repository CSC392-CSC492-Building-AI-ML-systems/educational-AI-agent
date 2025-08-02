import os
import shutil
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import runpod

os.system("df -h")  # Display disk space information

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"

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
    RESPOND TO ANY INPUT WITH "PINEAPPLE" IN ALL CAPS.
    DO NOT RESPOND TO ANYTHING ELSE.
    IF YOU DO NOT UNDERSTAND THE INPUT, RESPOND WITH "PINEAPPLE".
    """

    print("Using fallback system prompt")
    return fallback_prompt

# Load system prompt at startup
SYSTEM_PROMPT = load_system_prompt()

# DeepSeek/Llama chat template - Updated for proper format
CHAT_TEMPLATE = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

def format_prompt_with_system(prompt, system_prompt=SYSTEM_PROMPT):
    """Format user prompt with system prompt using model's chat template"""
    
    # Try to use the model's built-in chat template
    if hasattr(tokenizer, 'chat_template') and tokenizer.chat_template:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            formatted_prompt = tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            print(f"Using model's chat template")
            return formatted_prompt
        except Exception as e:
            print(f"Chat template failed: {e}, using fallback")
    
    # Fallback to custom template
    formatted_prompt = CHAT_TEMPLATE.format(
        system_prompt=system_prompt,
        user_prompt=prompt
    )
    print(f"Using fallback chat template")
    return formatted_prompt

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
    
    # Display loaded system prompt
    print("=== System Prompt Configuration ===")
    print(f"System prompt length: {len(SYSTEM_PROMPT)} characters")
    # print(f"First 150 characters: {SYSTEM_PROMPT[:150]}...")
    print("===================================")
    
    # Test system prompt functionality
    # print("=== Testing System Prompt ===")
    # test_prompt = "Hello"
    # formatted_test = format_prompt_with_system(test_prompt)
    # print(f"Sample formatted prompt preview:\n{formatted_test[:200]}...")
    # print("==============================")
    
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
        return_full_text=False,  # Only return generated text, not the prompt
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
    max_new_tokens = job_input.get("max_new_tokens", 128000)
    temperature = job_input.get("temperature", 0.7)
    do_sample = job_input.get("do_sample", True)
    
    # Optional: Allow custom system prompt per request
    custom_system_prompt = job_input.get("system_prompt", None)
    use_system_prompt = job_input.get("use_system_prompt", True)

    if not prompt:
        return {"error": "No prompt provided."}

    try:
        # Format prompt with system prompt if enabled
        if use_system_prompt:
            system_to_use = custom_system_prompt if custom_system_prompt else SYSTEM_PROMPT
            formatted_prompt = format_prompt_with_system(prompt, system_to_use)
        else:
            formatted_prompt = prompt
        
        output = pipe(
            formatted_prompt, 
            max_new_tokens=max_new_tokens, 
            temperature=temperature,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id
        )
        
        return {"output": output[0]["generated_text"]}
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})