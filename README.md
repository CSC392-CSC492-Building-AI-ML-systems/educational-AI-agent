# AutoDocs

Documentation and deployment are essential in software development, though many can agree that these tasks are often tedious and time-consuming. This is where AutoDocs comes in!

AutoDocs uses a **multi-model** approach to automate the documentation or deployment process, using only an Asciinema recording of the code session.

Led by Julia Longtin (https://github.com/julialongtin) of the Human Feedback Foundation, AutoDocs provides deep analysis of a given code session in a hierarchical format, and is part of a greater initiative to and commitment towards creating a truly open-source LLM, where all datasets are ethically sourced (not stolen!).

## Features
Each model utilizes an 8B parameter distillation of Deepseek R1, fine-tuned using LoRA, which was trained on an A100 GPU provided by Google Colab.
1. **Model 0 (Code Chunker)**: Splits code into \<event\> tags, representing unique actions within the code session.
2. **Model 1 (Annotator)**: Summarizes and provides a "depth" value to each event provided by Model 0. A "depth" is represented as: -1 (subevent), 0 (independent event), >=1 (exiting events).
3. **Model 3 (Dockerizer)**: A Dockerfile output of the commands run in the Asciinema recording.
4. **Parsing Scripts**: To avoid hallucination, outputs from models were further processed using parsers, avoiding complete regurgitation of input data. Currently, there exists Parser 0 (Asciinema to XML), Parser 1 (XML event grouping), and Parser 2 (XML summary insertion).

## Running AutoDocs
A raw Asciinema file is processed through a system (refer to System Architecture). All models can be loaded directly using the following code:
```
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("[model]")
model = AutoModelForCausalLM.from_pretrained("[model]")
```

### Parser 0
A Python script that takes in a raw Asciinema file, and converts it into an XML. Edit each variable in the script to coincide with the desired directory and filenames:
``` 
    # Define the input and output directories:
    input_dir = "educational-AI-agent/data/Model 0/raw"
    output_dir = "educational-AI-agent/data/Model 0/formatted"

    # Name of the file to parse (must exist in input_dir).
    input_file_name = "renee_rec2.cast"
    # Name for the resulting XML output.
    output_file_name = "renee_rec2.cast.xml"
```

### Model 0 (Code Chunker)
A fine-tuned model that will take in a converted XML (Parser 0 Output) and output a TXT with line numbers, printing "0" if the corresponding line should be the end of an event. Example:
```
1
2
3
0
4
5
6
7
0
```

Load the model directly with the earlier provided code snippet, available at: https://huggingface.co/bria7801/model-0

### Parser 1
A Python script that takes a converted XML (Parser 0 Output) and a TXT with line numbers for code chunks (Model 0 Output). It will split relevant line numbers using \<event\> tags, with an \<annotation\> tag created before the closing \<event\> tag. On a Terminal or Command Shell application, run:
```
    python parser1.py <xml> <txt>
```

### Model 1 (Annotator)
A fine-tuned model that will take an XML that is split by events (Parser 1 Output) and output a TXT with the hierarchical "depth" value and summary for each event. Example:
```
0
User connects to remote server via SSH using the command 'ssh 10.0.7.138' and enters password
-1
User changes their password on the remote server from '1M3T567!' to 'OpenYourHeartGPT'
1
User logs out of the SSH session and connection to the remote server is closed
0
User exits the terminal
```
Load the model directly with the earlier provided code snippet, available at: https://huggingface.co/bria7801/model-1

### Parser 2
A Python script that will take an XML that is split by events (Parser 1 Output) and a TXT with hierarchical "depth" values and event summaries (Model 1 output), and insert the latter data into the former. Edit the plain_text_list and parsed_xml_list variables with the desired filepaths.

### Model 3 (Dockerizer)
A fine-tuned model that will take an XML with summaries and depth values (Parser 2 Output) and output a Dockerfile that will run similar commands.

Load the model directly with the earlier provided code snippet, available at: https://huggingface.co/bria7801/model-3

## Future Extensions
1. **Dataset Expansion**: As all data is created by teams of Julia Longtin, and more data is needed to further increase the accuracy of the models.
2. **Markdown Output**: A model that is capable of outputting documentation, based on an annotated XML.
3. **TinTin++ Output**: A model that is capable of outputting TinTin++ code, based on the annotated XML.
4. **Frontend**: A frontend web app to improve user experience!

## System Architecture 
![System architecture](https://i.imgur.com/9iDfrbz.png)