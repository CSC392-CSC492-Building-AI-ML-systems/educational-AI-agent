import os
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import runpod

# Set environment variables to use network storage
os.environ['HF_HOME'] = '/runpod-volume/hf_cache'
os.environ['TRANSFORMERS_CACHE'] = '/runpod-volume/hf_cache'
os.environ['HF_HUB_CACHE'] = '/runpod-volume/hf_cache'

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"

def load_model():
    """Load model with optimized settings"""
    print(f"Loading model: {MODEL_ID}")
    
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        use_fast=True  # Use fast tokenizer if available
    )
    
    # Load model with memory optimizations
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        device_map="auto",  # Automatically distribute model across available devices
        torch_dtype="auto"  # Use optimal dtype
    )
    
    return model, tokenizer

# Load model and tokenizer
model, tokenizer = load_model()

# Create inference pipeline
print("Creating inference pipeline...")
pipe = TextGenerationPipeline(
    model=model, 
    tokenizer=tokenizer,
    device_map="auto"
)
print("Pipeline ready!")

def handler(job):
    job_input = job.get("input", {})
    prompt = job_input.get("prompt", "")
    max_new_tokens = job_input.get("max_new_tokens", 128)
    temperature = job_input.get("temperature", 0.7)
    do_sample = job_input.get("do_sample", True)

    if not prompt:
        return {"error": "No prompt provided."}

    try:
        # Generate with additional parameters for better control
        output = pipe(
            prompt, 
            max_new_tokens=max_new_tokens, 
            temperature=temperature,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id,
            return_full_text=False  # Only return generated text, not the prompt
        )
        
        return {"output": output[0]["generated_text"]}
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}"}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})