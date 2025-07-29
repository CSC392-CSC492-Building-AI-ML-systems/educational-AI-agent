#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import sys

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

def parse_recording(line_stream, strip_annotations=False):
    """
    Parse an asciinema recording line-by-line from stdin.
    
    The stream is expected to have a JSON header on the first non-empty line,
    and then one JSON array per line for each terminal event.
    
    :param line_stream: An iterable stream of input lines (e.g. sys.stdin).
    :param strip_annotations: If True, do not include annotations.
    :return: XML Element (root) of the generated XML tree.
    """
    root = None
    header_parsed = False

    for line in line_stream:
        line = line.strip()
        if not line:
            continue

        if not header_parsed:
            try:
                header = json.loads(line)
            except Exception as e:
                raise ValueError("Error parsing JSON header: " + str(e))

            root = ET.Element("recording")
            for key in ["version", "width", "height", "timestamp"]:
                if key in header:
                    root.set(key, str(header[key]))

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
                                ann_elem.text = remove_invalid_xml_chars(ann.get("text", ""))
            header_parsed = True
            continue

        try:
            event = json.loads(line)
        except Exception as e:
            print("Skipping line (could not parse JSON):", line, file=sys.stderr)
            continue

        if not isinstance(event, list) or len(event) < 3:
            continue

        timestamp, event_type, content = event[0], event[1], event[2]
        if event_type == "i":
            elem = ET.SubElement(root, "user_input")
        elif event_type == "o":
            elem = ET.SubElement(root, "system_output")
        else:
            continue

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
    # Read from stdin, write to stdout
    strip_annotations = True

    try:
        xml_root = parse_recording(sys.stdin, strip_annotations=strip_annotations)
    except Exception as e:
        print("Error parsing recording:", e, file=sys.stderr)
        return

    pretty_xml = prettify_xml(xml_root)
    print(pretty_xml)

if __name__ == "__main__":
    main()
