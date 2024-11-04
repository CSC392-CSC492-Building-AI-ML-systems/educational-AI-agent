import argparse
import os

# from pprint import pprint
# import bitsandbytes as bnb
import torch
# import torch.nn as nn
import transformers
from datasets import load_dataset
from peft import (
    LoraConfig,
    PeftConfig,
    PeftModel,
    get_peft_model,
    prepare_model_for_kbit_training
)
from transformers import (
    # AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    # BitsAndBytesConfig
)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
MODEL_NAME = "vilsonrodrigues/falcon-7b-instruct-sharded"

# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16
# )

def train_model(data):
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        trust_remote_code=True,
        # quantization_config=bnb_config
        torch_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    def print_trainable_parameters(model):
        """
      Prints the number of trainable parameters in the model.
      """
        trainable_params = 0
        all_param = 0
        for _, param in model.named_parameters():
            all_param += param.numel()
            if param.requires_grad:
                trainable_params += param.numel()
        print(
            f"trainable params: {trainable_params} || all params: {all_param} || trainables%: {100 * trainable_params / all_param}"
        )

    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["query_key_value"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, config)
    print_trainable_parameters(model)

    def generate_prompt(data_point):
        return f"""
    <human>: {data_point["User"]}
    <assistant>: {data_point["Prompt"]}
    """.strip()

    def generate_and_tokenize_prompt(data_point):
        full_prompt = generate_prompt(data_point)
        tokenized_full_prompt = tokenizer(full_prompt, padding=True, truncation=True)
        return tokenized_full_prompt

    data = data["train"].shuffle().map(generate_and_tokenize_prompt)

    training_args = transformers.TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        learning_rate=2e-4,
        fp16=True,
        save_total_limit=3,
        logging_steps=1,
        output_dir="experiments",
        optim="paged_adamw_8bit",
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
    )

    trainer = transformers.Trainer(
        model=model,
        train_dataset=data,
        args=training_args,
        data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    model.config.use_cache = False
    trainer.train()
    model.save_pretrained("trained-model")


def test_model(data):
    config = PeftConfig.from_pretrained("trained-model")
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model_name_or_path,
        return_dict=True,
        # quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

    tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
    tokenizer.pad_token = tokenizer.eos_token

    model = PeftModel.from_pretrained(model, "trained-model")

    generation_config = model.generation_config
    generation_config.max_new_tokens = 200
    generation_config.temperature = 0.7
    generation_config.top_p = 0.7
    generation_config.num_return_sequences = 1
    generation_config.pad_token_id = tokenizer.eos_token_id
    generation_config.eos_token_id = tokenizer.eos_token_id

    device = "cuda:0"

    prompt = f"""
    <human>: {data}
    <assistant>:
    """.strip()

    encoding = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = model.generate(
            input_ids=encoding.input_ids,
            attention_mask=encoding.attention_mask,
            generation_config=generation_config
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Make model.")
    parser.add_argument("input_file", help="Path to the data json.")
    parser.add_argument("train_or_test", help="Train or test?.")
    args = parser.parse_args()

    data = load_dataset('json', data_files={
        "train": args.input_file,
    })
    if args.train_or_test == "train":
        # Load and parse data
        train_model(data)
    else:
        for i in range(len(data["inputs"])):
            datapoint = data["inputs"][i]
            original_out = data["outputs"][i]
            out = test_model(datapoint)
            print(f"Out: {out}\n\nOriginal: {original_out}\n\n\n")

