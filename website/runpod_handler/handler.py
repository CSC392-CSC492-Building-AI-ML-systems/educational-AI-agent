from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline, BitsAndBytesConfig
import runpod
import torch

# Load model and tokenizer from Hugging Face
MODEL_ID = "cmdkp/autodocs_model_0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

# Configure 8-bit quantization with CPU offloading
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_enable_fp32_cpu_offload=True  # Enable CPU offloading for large models
)

# Load model with quantization and CPU offloading
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, 
    trust_remote_code=True,
    quantization_config=quantization_config,
    device_map="auto"  # Automatically distribute across GPU and CPU
)

# Create a text generation pipeline
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer)

# Define the handler function for RunPod
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

# Start the serverless worker
runpod.serverless.start({"handler": handler})
