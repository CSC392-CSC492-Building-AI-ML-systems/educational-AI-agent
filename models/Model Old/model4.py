import argparse
import os

import torch
import transformers
from datasets import load_dataset
from peft import (
    LoraConfig,
    PeftConfig,
    PeftModel,
#   get_peft_model,
#   prepare_model_for_kbit_training
)
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)
from trl import SFTConfig, SFTTrainer, DataCollatorForCompletionOnlyLM
# from unsloth import FastLanguageModel

max_seq_length = 4096  # Supports automatic RoPE Scaling, so choose any number
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
MODEL_NAME = "01-ai/Yi-6B"


def train_model(data):

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    assert tokenizer.pad_token != tokenizer.eos_token

    special_tokens = {
        "additional_special_tokens": ["<history>", "<entry>", "<input>", "<output>", "<annotation>", "<current-entry>",
                                      "</history>", "</entry>", "</input>", "</output>", "</annotation>",
                                      "</current-entry>", "[BLANK]", "[NO_OUTPUT]", "<data-piece>", "</data-piece>"]
    }
    tokenizer.add_special_tokens(special_tokens)
    model.resize_token_embeddings(len(tokenizer))

    config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # Do model patching and add fast LoRA weights

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

    print_trainable_parameters(model)
    print("CUDA available:", torch.cuda.is_available())
    print("Number of GPUs:", torch.cuda.device_count())

    def generate_prompt(example):
        return {"text": """### Human: You are given a recording of someone working on the terminal, such as on "
                "some code. There is a history, marked by <history> and </history> of entries, "
                "marked by <entry> and </entry>, signifying a block of the terminal"
                "inputs and outputs in a certain period of time, with entry with its own "
                "annotations, marked by <annotation> and </annotation> on"
                "multiple levels. An annotation can repeat the previous entry's annotation on "
                "some or all of the levels. An annotation can be empty. There is a current entry, "
                "marked by <current-entry> and </current-entry>, at the end, with one of the"
                "annotations being [BLANK]. Your task is to predict what that annotation should "
                "be, or to return [NO-OUTPUT] if it should be empty. Do not output anything else, "
                "just the annotation, or [NO-OUTPUT].\n""" + example["prompt"] +
                "\n\n### Assistant: " + example["chosen"] + tokenizer.eos_token}

    dataset = data["train"].shuffle().map(generate_prompt, remove_columns=["prompt", "chosen"])

    response_template = "### Assistant:"
    collator = DataCollatorForCompletionOnlyLM(response_template=response_template, tokenizer=tokenizer)

    training_args = SFTConfig(output_dir="./output", max_seq_length=max_seq_length)

    # training_args = transformers.TrainingArguments(
    #     per_device_train_batch_size=1,
    #     gradient_accumulation_steps=4,
    #     num_train_epochs=1.5,
    #     learning_rate=1e-4,
    #     fp16=True,
    #     save_total_limit=3,
    #     logging_steps=1,
    #     output_dir="experiments",
    #     optim="adamw_hf",
    #     lr_scheduler_type="cosine",
    #     warmup_ratio=0.05,
    # )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=collator,
        peft_config=config
    )
    trainer.train()

    model.save_pretrained("trained-model")
    tokenizer.save_pretrained("trained-model")


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

    tokenizer = AutoTokenizer.from_pretrained("trained-model")
    model.resize_token_embeddings(len(tokenizer))
    model = PeftModel.from_pretrained(model, "trained-model")

    generation_config = model.generation_config
    generation_config.max_new_tokens = 200
    generation_config.temperature = 0.7
    generation_config.top_p = 0.7
    generation_config.num_return_sequences = 1
    generation_config.pad_token_id = tokenizer.pad_token_id
    generation_config.eos_token_id = tokenizer.eos_token_id


    for datum in data:
        datapoint = datum["User"]
        original_out = datum["Prompt"]

        prompt = f"""<human>: This is a snapshot of a recording of someone working on something in the terminal, such as some code. There is a history of entries, which compile inputs and outputs, and each are annotated, at possibly multiple levels. There is a special entry at the end, which is the current snapshot's entry. One of the annotation levels has a [BLANK], and you should output what that level's annotation should be, based on the data.

{datapoint}

<assistant>: """

        encoding = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.inference_mode():
            outputs = model.generate(
                input_ids=encoding.input_ids,
                attention_mask=encoding.attention_mask,
                generation_config=generation_config
            )

        out = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Out: {out}\n\nOriginal: {original_out}\n\n\n")

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
        test_model(data["train"])

