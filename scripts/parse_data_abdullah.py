import json
import re
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from xml.sax.saxutils import escape
import argparse
import logging
from transformers import AutoTokenizer
import os

# from model.model import outputs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Annotation:
    # group: str
    beginning: float  # in milliseconds
    end: float  # in milliseconds
    text: str
    level: int
    # entry_list: List['Entry'] = field(default_factory=list)


@dataclass
class Entry:
    input: str = ""
    output: str = ""
    # start_time: float = 0.0
    # end_time: float = 0.0
    annotations: List[Annotation] = field(default_factory=list)


@dataclass
class History:
    entries: List[Entry] = field(default_factory=list)


@dataclass
class CurrentEntry:
    entry: Entry


@dataclass
class DataPiece:
    history: History
    current_entry: Optional[CurrentEntry]


class AnnotationProcessor:
    def __init__(self, input_file: str, output_dir: str, token_limit: int = 512,
                 tokenizer_name: str = "t5-large", context_size: int = 50):
        """
        Initializes the AnnotationProcessor.
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.annotations: List[Annotation] = []
        self.events: List[Dict] = []
        self.num_levels = 0

        self.history = History()
        self.current_entry: Optional[CurrentEntry] = None

        self.token_limit = token_limit
        self.context_size = context_size

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_fast=True)

        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.control_chars = re.compile(r'[\r\n\t\x00-\x1F\x7F-\x9F]')
        self.punctuation_spacing = re.compile(r'([.,!?])(\S)')
        self.multiple_spaces = re.compile(r' +')
        self.multiple_periods = re.compile(r'\.{2,}')
        self.special_characters = re.compile(r'[^\w\s.,!?<>()\-\[\]]')  # Keep [sudo] 
        self.ip_address = re.compile(r'(\b\d{1,3}(?:\.\d{1,3}){3}\b)')

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    # ******************************************************************************************************************

    def parse_input(self):
        """
        Parses the input file to extract annotations and events.
        Events are just the lines in the recording files following the json meta-data
        i.e, they look like this: [timestamp, "i" or "o", "text"]
        """
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            logger.info(f"Successfully read {len(lines)} lines from {self.input_file}.")
        except FileNotFoundError:
            logger.error(f"Input file {self.input_file} not found.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            sys.exit(1)

        # Parse the JSON object at the beginning
        json_lines = []
        brace_count = 0
        json_started = False

        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('{'):
                json_started = True
            if json_started:
                json_lines.append(line)
                brace_count += line.count('{')
                brace_count -= line.count('}')
                if brace_count == 0:
                    break

        try:
            json_data = json.loads(''.join(json_lines))
            logger.info("Successfully parsed JSON metadata.")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            sys.exit(1)

        # Extract annotations
        layers = json_data.get("librecode_annotations", {}).get("layers", [])
        self.num_levels = len(layers)
        for level, layer in enumerate(layers):
            for ann in layer.get("annotations", []):
                annotation = Annotation(
                    # group=ann.get("group", ""),
                    beginning=ann.get("beginning", 0.0),  # in milliseconds
                    end=ann.get("end", 0.0),  # in milliseconds
                    text=ann.get("text", ""),
                    level=level
                )
                self.annotations.append(annotation)
        logger.info(f"Extracted {len(self.annotations)} annotations.")

        # Parse the remaining lines as events
        event_pattern = re.compile(r'^\[(\d+\.\d+),\s*"([io])",\s*"(.*)"]$')
        for line in lines[len(json_lines):]:
            line = line.strip()
            if not line:
                continue
            match = event_pattern.match(line)
            if match:
                timestamp_sec = float(match.group(1))
                timestamp_ms = timestamp_sec * 1000  # Convert to milliseconds
                event_type = match.group(2)
                # Decode Unicode escape sequences
                try:
                    text = bytes(match.group(3), "utf-8").decode("unicode_escape")
                except UnicodeDecodeError:
                    text = match.group(3)  # If decoding fails, keep original
                self.events.append({
                    "timestamp": timestamp_ms,
                    "type": event_type,
                    "text": text
                })
            else:
                logger.warning(f"Line didn't match event pattern and was skipped: {line}")

        logger.info(f"Parsed {len(self.events)} events.")

    def clean_text(self, text: str) -> str:
        """
        Cleans the text by removing characters that aren't useful TOGGLE
        """
        text = self.ansi_escape.sub('', text)
        text = self.control_chars.sub('', text)
        text = self.multiple_periods.sub('...', text)
        text = self.punctuation_spacing.sub(r'\1 \2', text)
        text = self.multiple_spaces.sub(' ', text)
        text = self.ip_address.sub(r'\1', text)
        text = self.special_characters.sub('', text)
        text = text.strip()
        return text

    # ******************************************************************************************************************

    def organize_entries(self):
        """
        Organizes events into entries by pairing user inputs with corresponding outputs.
        Each entry now records its start and end times to enable overlapping with annotations.
        """
        times = [0.0]
        for annotation in self.annotations:
            times.append(annotation.beginning)
            times.append(annotation.end)
        times.append(self.events[-1]["timestamp"])
        times.sort()

        for i in range(len(times) - 1):
            start_time = times[i]
            end_time = times[i + 1]
            inputs = ''.join([event["text"] for event in self.events
                              if event["type"] == 'i' and start_time <= event["timestamp"] < end_time])
            outputs = ''.join([event["text"] for event in self.events
                               if event["type"] == 'o' and start_time <= event["timestamp"] < end_time])
            if not inputs and not outputs:
                continue

            entry = Entry(
                input=inputs,
                output=outputs
            )
            # Associate annotations based on overlapping
            entry.annotations = [
                ann for ann in self.annotations
                if (start_time < ann.end and ann.beginning < end_time)
            ]
            # # Add the entry to the annotations' entry_list
            # for ann in entry.annotations:
            #     ann.entry_list.append(entry)
            self.history.entries.append(entry)

        # state = 'idle'  # Possible states: 'idle', 'inputting', 'waiting_output'
        # current_input = []
        # current_output = []
        # entry_start_time = 0.0
        # entry_end_time = 0.0
        #
        # def finalize_entry(cleaned_input, cleaned_output, start_time, end_time):
        #     if cleaned_output:
        #         entry = Entry(
        #             input=cleaned_input,
        #             output=cleaned_output,
        #             start_time=start_time,
        #             end_time=end_time
        #         )
        #         # Associate annotations based on overlapping
        #         entry.annotations = [
        #             ann for ann in self.annotations
        #             if (start_time <= ann.end <= end_time or start_time <= ann.beginning <= end_time)
        #         ]
        #         # Add the entry to the annotations' entry_list
        #         for ann in entry.annotations:
        #             ann.entry_list.append(entry)
        #         self.history.entries.append(entry)
        #
        # def is_echo(input_str, output_str):
        #     return input_str.endswith(output_str)
        #
        # for event in self.events:
        #     timestamp = event["timestamp"]
        #     event_type = event["type"]
        #     text = event["text"]
        #
        #     if state == 'idle':
        #         if event_type == 'i':
        #             if text in ['\r', '\n']:
        #                 # Enter pressed without any input; possible prompt
        #                 state = 'waiting_output'
        #             else:
        #                 state = 'inputting'
        #                 current_input.append(text)
        #                 entry_start_time = timestamp  # Start time recorded
        #         elif event_type == 'o':
        #             cleaned_output = self.clean_text(text)
        #             if cleaned_output:
        #                 # Output without prior input
        #                 finalize_entry("", cleaned_output, timestamp, timestamp)
        #     elif state == 'inputting':
        #         if event_type == 'i':
        #             if text in ['\r', '\n']:
        #                 # End of input; wait for output
        #                 state = 'waiting_output'
        #                 entry_end_time = timestamp  # End time recorded
        #             else:
        #                 current_input.append(text)
        #         elif event_type == 'o':
        #             input_str = ''.join(current_input)
        #             if not is_echo(input_str, text):
        #                 current_output.append(text)
        #     elif state == 'waiting_output':
        #         if event_type == 'i':
        #             if text not in ['\r', '\n']:
        #                 # New input started. Finalize previous entry
        #                 cleaned_input = self.clean_text(''.join(current_input))
        #                 cleaned_output = self.clean_text(''.join(current_output))
        #                 finalize_entry(cleaned_input, cleaned_output, entry_start_time, entry_end_time)
        #                 # Start capturing new input
        #                 current_input = [text]
        #                 current_output = []
        #                 state = 'inputting'
        #                 entry_start_time = timestamp  # New entry start time
        #         elif event_type == 'o':
        #             if text in ['\r', '\n']:
        #                 # Possibly end of output; update entry_end_time
        #                 entry_end_time = timestamp
        #             else:
        #                 current_output.append(text)
        #
        # # Finalize any remaining entry after processing all events
        # if state in ['waiting_output', 'inputting'] and (current_input or current_output):
        #     cleaned_input = self.clean_text(''.join(current_input))
        #     cleaned_output = self.clean_text(''.join(current_output))
        #     last_timestamp = self.events[-1]["timestamp"] if self.events else 0.0
        #     finalize_entry(cleaned_input, cleaned_output, entry_start_time, last_timestamp)

        logger.info(f"Organized {len(self.history.entries)} entries.")

    # ******************************************************************************************************************

    # def link_current_entry(self, entry_index: int) -> Optional[CurrentEntry]:
    #     """
    #     Links the entry at the given index as the current entry if valid.
    #     """
    #     if 0 <= entry_index < len(self.history.entries):
    #         logger.info(f"Linked entry at index {entry_index} as the current entry.")
    #         return CurrentEntry(entry=self.history.entries[entry_index])
    #     logger.warning(f"Entry index {entry_index} is out of bounds.")
    #     return None

    def escape_special_chars(self, text: str) -> str:
        """Escapes XML special characters for valid XML formatting."""
        return text
        # return escape(text)    TOGGLE

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def generate_data_pieces(self):
        """
        Generates and saves data-pieces as XML files, each containing a history of 
        context_size entries and the current entry, within the token limit.
        """
        if not self.history.entries:
            logger.warning("No entries to process into data-pieces.")
            return

        final = []
        for i, current_entry in enumerate(self.history.entries):
            # Get the context (previous entries) and create the data-piece
            history_entries = self.history.entries[:i]
            # history_entries = self.history.entries[max(0, i - self.context_size):i]
            data_piece = DataPiece(
                history=History(entries=history_entries),
                current_entry=CurrentEntry(entry=current_entry)
            )

            # Generate and save XML
            finals = self.generate_xml(data_piece)
            final.extend(finals)
            # data_piece_filename = f"data_piece_{i + 1}.xml"
            # data_piece_path = os.path.join(self.output_dir, data_piece_filename)
            #
            # try:
            #     with open(data_piece_path, 'w', encoding='utf-8') as outfile:
            #         outfile.write(xml_output)
            #     logger.info(f"Data-piece {i + 1} saved to {data_piece_path}.")
            # except Exception as e:
            #     logger.error(f"Error writing data-piece {i + 1} to file: {e}")
        return final

    # ******************************************************************************************************************

    def generate_xml(self, data_piece: DataPiece) -> str:
        """
        Generates XML for a data-piece, including history and current entry, within the token limit.
        """
        # Helper to clean and escape text
        def clean_and_escape(text: str) -> str:
            return self.escape_special_chars(self.clean_text(text))

        final = []
        for curr in range(self.num_levels):
            xml_parts = ["<data-piece>", "<history>", "</history>"]

            # Process current entry
            output_ann = "[NO_OUTPUT]"
            if data_piece.current_entry:
                entry = data_piece.current_entry.entry
                annotations_texts = [""] * self.num_levels
                annotations_texts[curr] = "[BLANK]"
                for ann in entry.annotations:
                    if ann.level == curr:
                        output_ann = ann.text
                    else:
                        annotations_texts[ann.level] = clean_and_escape(ann.text)

                annotations_xml = ""
                for ann_text in annotations_texts:
                    annotations_xml += f"<annotation>{ann_text}</annotation>"
                xml_parts.append(
                    f"<current-entry>"
                    f"<entry>"
                    f"<input>{clean_and_escape(entry.input)}</input>"
                    f"<output>{clean_and_escape(entry.output)}</output>"
                    f"{annotations_xml}"
                    f"</entry>"
                    f"</current-entry>"
                )

            xml_parts.append("</data-piece>")

            # Process history entries
            for entry in data_piece.history.entries[::-1]:
                # entry_tokens = (self.count_tokens(entry.input) +
                #                 self.count_tokens(entry.output) +
                #                 sum(self.count_tokens(ann.text) for ann in entry.annotations))
                #
                # if total_tokens + entry_tokens > max_tokens:
                #     logger.info("Token limit reached. Stopping further entries.")
                #     break

                # Add entry to XML
                annotations_texts = [""] * self.num_levels
                for ann in entry.annotations:
                    annotations_texts[ann.level] = clean_and_escape(ann.text)
                annotations_xml = ""
                for ann_text in annotations_texts:
                    annotations_xml += f"<annotation>{ann_text}</annotation>"

                xml_parts.insert(
                        2,
                        f"<entry>"
                        f"<input>{clean_and_escape(entry.input)}</input>"
                        f"<output>{clean_and_escape(entry.output)}</output>"
                        f"{annotations_xml}"
                        f"</entry>"
                )

                # current_tokens = self.count_tokens("\n".join(xml_parts))
                # if current_tokens > self.token_limit:
                #     xml_parts.pop(2)
                #     logger.info("Token limit reached. Stopping further entries.")
                #     break

                # total_tokens += entry_tokens

            final.append({"User": "".join(xml_parts), "Prompt": output_ann})
        return final

    def process(self):
        """
        Executes the parsing, organizing, and generation of data-pieces.
        """
        self.parse_input()
        self.organize_entries()
        return self.generate_data_pieces()


def parse_and_save_file(input_file: str, output_dir: str, token_limit: int = 512, tokenizer_name: str = "t5-large",
                        context_size: int = 50):
    """
    Parses an asciinema recording and saves XML data-pieces to the output directory.

    Args:
        input_file (str): Path to the asciinema recording file.
        output_dir (str): Directory to save data-pieces.
        token_limit (int, optional): Max tokens per data-piece.
        tokenizer_name (str, optional): Tokenizer for token counting. Defaults to "t5-large".
        context_size (int, optional): Context entries per data-piece. Defaults to 5.
    """
    return AnnotationProcessor(input_file, output_dir, token_limit, tokenizer_name, context_size).process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process asciinema recordings into XML data-pieces.")
    parser.add_argument("input_file", help="Path to the asciinema recording.")
    parser.add_argument("output_dir", help="Directory for XML data-pieces.")
    parser.add_argument("--token_limit", type=int, default=512, help="Max tokens per data-piece.")
    parser.add_argument("--tokenizer", type=str, default="t5-large", help="Tokenizer for token counting.")
    parser.add_argument("--context_size", type=int, default=50, help="Number of context entries.")
    args = parser.parse_args()

    final = []

    for file in os.scandir(args.input_file):
        filename = file.path
        finals = parse_and_save_file(filename, args.output_dir, args.token_limit, args.tokenizer,
                                              args.context_size)
        final.extend(finals)

    json.dump(final, open(os.path.join(args.output_dir, "data3.json"), "w"), indent=4)

    # take a directory
    # parse all files in the directory
    # take the output and put it in 2 lists: inputs and outputs. inputs have a blank for each annotation
    # output is the filling of the blank
    # save into one json with two lists
    # make 2 jsons, one with cleaned and one without
    # train on both and see
    # tokenize special and don't



