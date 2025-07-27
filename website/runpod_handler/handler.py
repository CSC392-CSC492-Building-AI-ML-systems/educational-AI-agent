from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import runpod
import os

MODEL_ID = "nuhgooyin/autodocs_model_0_no_gguf"
NETWORK_MODEL_PATH = "/runpod-volume/autodocs_model_0"

# Check if model exists on network storage, otherwise download
if os.path.exists(NETWORK_MODEL_PATH):
    tokenizer = AutoTokenizer.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(NETWORK_MODEL_PATH, trust_remote_code=True)
else:
    # Download and save to network storage
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True)
    os.makedirs(NETWORK_MODEL_PATH, exist_ok=True)
    tokenizer.save_pretrained(NETWORK_MODEL_PATH)
    model.save_pretrained(NETWORK_MODEL_PATH)

# Create pipeline - this loads model weights into GPU memory
pipe = TextGenerationPipeline(model=model, tokenizer=tokenizer, device=0)

def handler(event):
    # Inference happens on worker GPU
    input_data = event.get("input", {})
    prompt = input_data.get("prompt", "")
    max_new_tokens = input_data.get("max_new_tokens", 128)
    temperature = input_data.get("temperature", 0.7)

    if not prompt:
        return {"error": "No prompt provided."}

    output = pipe(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
    return {"output": output[0]["generated_text"]}

runpod.serverless.start({"handler": handler})
