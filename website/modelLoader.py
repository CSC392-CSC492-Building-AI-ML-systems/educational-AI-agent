from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Input prompt
prompt = ""

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt")

# Generate output
outputs = model.generate(inputs["input_ids"], max_length=50, num_return_sequences=1)

# Decode and print the result
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)
