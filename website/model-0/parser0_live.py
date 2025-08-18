# !/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import os
import sys
import argparse

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

def parse_recording_from_string(text, strip_annotations=False):
    """
    Parse an asciinema recording from a string (instead of file).
    """
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("No input provided")

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
    for line in lines[1:]:
        try:
            event = json.loads(line)
        except Exception:
            continue
        if not isinstance(event, list) or len(event) < 3:
            continue

        timestamp, event_type, content = event[0], event[1], event[2]
        if event_type == "i":
            elem = ET.SubElement(root, "user_input")
            elem.set("timestamp", str(timestamp))
            elem.text = remove_invalid_xml_chars(content)
        elif event_type == "o":
            elem = ET.SubElement(root, "system_output")
            elem.set("timestamp", str(timestamp))
            elem.text = remove_invalid_xml_chars(content)

    return root

def prettify_xml(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def main():
    header_printed = False
    print("<!-- Starting live recording session -->", file=sys.stderr)

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except Exception as e:
                print(f"<!-- Error parsing JSON: {e} -->", file=sys.stderr)
                continue

            # First line = header
            if isinstance(obj, dict) and not header_printed:
                version = obj.get("version", "2")
                width = obj.get("width", 80)
                height = obj.get("height", 24)
                ts = obj.get("timestamp", 0)
                print(f'<?xml version="1.0" ?>')
                print(f'<recording version="{version}" width="{width}" height="{height}" timestamp="{ts}">')
                header_printed = True
                sys.stdout.flush()
                continue

            # Later lines = events
            if isinstance(obj, list) and len(obj) == 3:
                t, typ, data = obj
                data = remove_invalid_xml_chars(data)

                if typ == "o":
                    print(f'  <system_output timestamp="{t}">{data}</system_output>')
                elif typ == "i":
                    print(f'  <user_input timestamp="{t}">{data}</user_input>')
                else:
                    print(f'  <!-- Unknown type {typ} -->')

                sys.stdout.flush()

        # When stdin closes → finish recording
        if header_printed:
            print("</recording>")
            sys.stdout.flush()

    except KeyboardInterrupt:
        if header_printed:
            print("</recording>")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
