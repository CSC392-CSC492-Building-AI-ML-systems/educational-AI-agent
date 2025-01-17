# -*- coding: utf-8 -*-
"""CSC392-MODEL-2-INFERENCE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kNXI35jR0QRum8Vqa4jTTdiwj7s_-sFI

**GET FINE-TUNED MODEL FROM HUGGINGFACE**
"""

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("cfstar188/csc392-model-2-final")
model = AutoModelForCausalLM.from_pretrained("cfstar188/csc392-model-2-final")

!pip3 install torch

import torch

device = torch.device("cuda")
model.cuda()

"""**FUNCTIONS FOR INFERENCING**"""

import time

def get_completion(annotations: str, model, tokenizer) -> str:
    device = "cuda:0"

    # Start measuring time
    start_time = time.time()

    # Format the prompt
    prompt_template = """"
        <start_of_turn>user
        Based on the following annotated Asciinema recording:
        {annotations}
        Generate a single cohesive Markdown file that explains and summarizes the entire process from the Asciinema recording.
        The summary should focus on:
        * Describing the context of each action.
        * Clearly explaining why the action was used, what the action does, and the outcome of this action.
        * Focus on making the documentation informative enough to be easily followed, capturing the step-by-step workflow as demonstrated in the recording, without using generic phrases.

        In the Markdown file, I want the following:
        * The main title should be preceded with a # and section titles should be preceded with ##.
        * End the markdown file with a 'Key Takeaways' section that summarizes the main points of the recording.
        <end_of_turn>\n
        <start_of_turn>model
    """
    prompt = prompt_template.format(annotations=annotations)

    # Tokenize the prompt
    encodings = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)

    # Move inputs to the correct device
    model_inputs = encodings.to(device)

    # Generate the model's response
    generated_ids = model.generate(**model_inputs, max_new_tokens=int(len(annotations)//1.5), do_sample=True, pad_token_id=tokenizer.eos_token_id)

    # Decode the output tokens
    decoded = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    # End timing
    end_time = time.time()

    # Print time
    print(f"Total time: {end_time - start_time:.2f} seconds")

    # Print and return the result
    return decoded

import re
import json

def parse_output(input_string):
    # Find the position of the word "model"
    index_model = input_string.find("model")

    # If "model" is found, get the substring after it

    if index_model == -1:
      return "model keyword not found"
    else:
        input_string = input_string[index_model+5:] # get all characters after the word "model"

    # Find the position of the substring "Key Takeaways"
    index_takeaways = input_string.find("Key Takeaways")

    # If "Key Takeaways" is found, extract it and the next 5 lines
    if index_takeaways != -1:
        # Extract the substring starting from "Key Takeaways"
        takeaways_substring = input_string[index_takeaways:]

        # Split into lines and get the first lines after Key Takeaways
        lines = takeaways_substring.splitlines()

        # Find the index of the first blank line
        blank_line_index = 0
        for index, line in enumerate(lines):
            if line == '':
                blank_line_index = index
                break

        lines = lines[:blank_line_index]

        # Join the lines back into a string
        return (input_string[:index_takeaways] + "\n".join(lines)).strip()
    else: # if Ket Takeaways is not found, just return the whole string
        return input_string

def save_markdown(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

"""
Return an array of all <data-piece>...</data-piece> in the input string
"""
def extract_data_pieces(input_string):
    # Define the regex pattern to match <data-piece>...</data-piece>
    pattern = r"<data-piece>.*?</data-piece>"
    # Use re.findall to extract all matches
    data_pieces = re.findall(pattern, input_string, re.DOTALL)
    return data_pieces

"""
Precondition: file_path is a json file with an "annotation" key that stores an annotated session
Postcondition: Generates the markdown summary file in the same directory as the json file
"""
def generate_markdown(file_path):
  json_content = None
  with open(file_path, 'r') as f:
    json_content = json.load(f)
    # Check if json_content is a dictionary and extract the "annotation" key
    if isinstance(json_content, dict):
        json_content = json_content.get("annotation")

        json_content = extract_data_pieces(json_content)
        parsed_output = ""
        for content in json_content:
          completion = get_completion(content, model=model, tokenizer=tokenizer)
          parsed_output += parse_output(completion) + "\n\n"

        print(parsed_output)
        inference_file_name = file_path.replace(".json", "_inference.md")
        save_markdown(inference_file_name, parsed_output)

"""**TESTS**"""

generate_markdown("49/data.json")

generate_markdown("48/data.json")

generate_markdown("45/data.json")

generate_markdown("34/data.json")

generate_markdown("46/data.json")