from unsloth import FastLanguageModel
from transformers import AutoTokenizer
import torch


BASE_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
ADAPTER_PATH = "./model_0"

# load the model and tokenizer
# Note: trust_remote_code=True is used to allow loading custom code from the model repository on Hugging Face

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = BASE_MODEL,
    max_seq_length = 1024 * 10,
    dtype = None,
    load_in_4bit = True,
    trust_remote_code = True,
)


# Load the adapter
# Note: The adapter is a fine-tuned version of the base model, which can be used for specific tasks or domains.
# The adapter is loaded from a local path, but it can also be loaded from a remote repository on Hugging Face.
model = FastLanguageModel.load_adapter(model, ADAPTER_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# ---- Generation function ----
def generate_response(prompt, max_tokens=1200):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(
        input_ids=input_ids,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        top_k=50,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# ---- Example usage ----
if __name__ == "__main__":
	prompt = ""
	response = generate_response(prompt)
	print(f"Prompt: {prompt}")
	print(f"Response: {response}")