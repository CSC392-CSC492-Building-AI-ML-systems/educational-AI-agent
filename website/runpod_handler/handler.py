import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"

# Initialize model and tokenizer
try:
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"  # This goes in from_pretrained, not the pipeline
    )
    
    print("Creating pipeline...")
    pipe = TextGenerationPipeline(
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
    print("Pipeline created successfully")
except Exception as e:
    print(f"Initialization failed: {str(e)}")
    raise

def handler(job):
    """Handle inference requests"""
    try:
        job_input = job.get("input", {})
        prompt = job_input.get("prompt", "")
        
        if not prompt:
            return {"error": "No prompt provided"}
        
        # Generation parameters
        gen_params = {
            "max_new_tokens": 100,
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "repetition_penalty": 1.2,
            "do_sample": True
        }
        
        # Generate and process output
        output = pipe(prompt, **gen_params)
        raw_output = output[0]["generated_text"]
        
        # Simple number extraction
        numbers = []
        for line in raw_output.split('\n'):
            line = line.strip()
            if line.isdigit() or line == '0':
                numbers.append(line)
        
        return {"output": "\n".join(numbers) if numbers else "1"}
    
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

if __name__ == "__main__":
    import runpod
    runpod.serverless.start({"handler": handler})