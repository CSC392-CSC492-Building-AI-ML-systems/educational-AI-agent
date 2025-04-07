# !/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import os

def remove_invalid_xml_chars(s):
    """
    Remove characters that are invalid in XML 1.0.
    Allowed characters are:
      - #x9 (tab)
      - #xA (newline)
      - #xD (carriage return)
      - #x20 to #xD7FF
      - #xE000 to #xFFFD
      - #x10000 to #x10FFFF
    This function removes characters in the range:
      #x00-#x08, #x0B-#x0C, and #x0E-#x1F.
    """
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', s)

def parse_recording(file_path, strip_annotations=False):
    """
    Parse an asciinema recording file and return an XML ElementTree root.
    
    The file is expected to have a JSON header on the first non-empty line,
    and then one JSON array per line for each terminal event.
    
    :param file_path: Path to the asciinema file.
    :param strip_annotations: If True, do not include annotations.
    :return: XML Element (root) of the generated XML tree.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read all non-empty lines.
        lines = [line for line in f if line.strip()]
    
    try:
        header = json.loads(lines[0])
    except Exception as e:
        raise ValueError("Error parsing JSON header: " + str(e))
    
    # Create the XML root element and add header attributes if available.
    root = ET.Element("recording")
    for key in ["version", "width", "height", "timestamp"]:
        if key in header:
            root.set(key, str(header[key]))
    
    # Add annotations (if any) unless we are stripping them.
    if not strip_annotations and "librecode_annotations" in header:
        annotations_data = header["librecode_annotations"]
        annotations_elem = ET.SubElement(root, "annotations")
        if "layers" in annotations_data:
            for layer in annotations_data["layers"]:
                layer_elem = ET.SubElement(annotations_elem, "layer")
                if "title" in layer:
                    layer_elem.set("title", layer["title"])
                if "annotations" in layer:
                    for ann in layer["annotations"]:
                        ann_elem = ET.SubElement(layer_elem, "annotation")
                        if "beginning" in ann:
                            ann_elem.set("beginning", str(ann["beginning"]))
                        if "end" in ann:
                            ann_elem.set("end", str(ann["end"]))
                        # Remove any invalid XML characters from the annotation text.
                        ann_elem.text = remove_invalid_xml_chars(ann.get("text", ""))
    
    # Process each terminal event (each subsequent line).
    # Each event is expected to be a JSON array: [timestamp, type, text]
    for line in lines[1:]:
        try:
            event = json.loads(line)
        except Exception as e:
            print("Skipping line (could not parse JSON):", line)
            continue
        
        if not isinstance(event, list) or len(event) < 3:
            continue

        timestamp, event_type, content = event[0], event[1], event[2]
        # Depending on the event type, create a corresponding XML element.
        if event_type == "i":
            elem = ET.SubElement(root, "user_input")
            elem.set("timestamp", str(timestamp))
            elem.text = remove_invalid_xml_chars(content)
        elif event_type == "o":
            elem = ET.SubElement(root, "system_output")
            elem.set("timestamp", str(timestamp))
            elem.text = remove_invalid_xml_chars(content)
        else:
            # Unknown event type; skip.
            continue

    return root

def prettify_xml(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def main():
    # Define the input and output directories:
    input_dir = "educational-AI-agent/data/Model 0/raw"
    output_dir = "educational-AI-agent/data/Model 0/formatted"

    # Name of the file to parse (must exist in input_dir).
    input_file_name = "renee_rec2.cast"
    # Name for the resulting XML output.
    output_file_name = "renee_rec2.cast.xml"

    # Construct full paths.
    input_file = os.path.join(input_dir, input_file_name)
    output_file = os.path.join(output_dir, output_file_name)

    # Set to True if you want to remove annotations from the output.
    strip_annotations = True

    # Parse the recording and handle errors.
    try:
        xml_root = parse_recording(input_file, strip_annotations=strip_annotations)
    except Exception as e:
        print("Error parsing recording:", e)
        return

    # Generate a pretty-printed XML string.
    pretty_xml = prettify_xml(xml_root)

    # Ensure the output directory exists (in case it doesn't).
    os.makedirs(output_dir, exist_ok=True)

    # Write the XML to the output file.
    with open(output_file, "w", encoding="utf-8") as out_f:
        out_f.write(pretty_xml)
    print(f"XML written to {output_file}")

if __name__ == "__main__":
    main()
