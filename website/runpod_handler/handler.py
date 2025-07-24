from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import runpod

# Load model and tokenizer from Hugging Face
MODEL_ID = "cmdkp/autodocs_model_0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True)

# Create a text generation pipeline
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer, device=0)

# Define the handler function for RunPod
def handler(event):
    input_data = event.get("input", {})
    prompt = input_data.get("prompt", "")
    max_new_tokens = input_data.get("max_new_tokens", 128)  # Default to 128 tokens for now
    temperature = input_data.get("temperature", 0.7)  # Default temperature for now

    if not prompt:
        return {"error": "No prompt provided."}

    output = pipe(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
    return {"output": output[0]["generated_text"]}

# Start the serverless worker
runpod.serverless.start({"handler": handler})
