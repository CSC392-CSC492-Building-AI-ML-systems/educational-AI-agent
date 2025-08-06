import sys
import os
from glob import glob

def process_file(xml, txt, out):
    print(f"Processing {xml} and {txt}")

    with open(xml, "r", encoding="utf-8") as f:
        xml_data = f.readlines()

    with open(txt, "r", encoding="utf-8") as f:
        counter = [int(line.strip()) for line in f]

    breaks = set(counter[i-1] for i in range(len(counter)) if counter[i] == 0)

    xml_parsed = []
    for i, line in enumerate(xml_data):
        if i in breaks:
            xml_parsed.append("<annotation>\n</annotation>\n</event>\n<event depth=\"-2\">\n")
        elif i == 2:
            xml_parsed.append("<event depth=\"-2\">\n")
        elif i == len(xml_data) - 1:
            xml_parsed.append("<annotation>\n</annotation>\n</event>\n")
        xml_parsed.append(line)

    with open(out, "w", encoding="utf-8") as f:
        f.writelines(xml_parsed)

    print(f"Parsed XML saved as {out}")


if __name__ == "__main__":
    xml_dir = "expanded_dataset\model_0\inputs"
    txt_dir = "expanded_dataset\model_0\outputs"
    output_dir = "expanded_dataset\model_1\inputs"
    os.makedirs(output_dir, exist_ok=True)

    # Get all XML files ending with .rec.xml
    xml_files = glob(os.path.join(xml_dir, "*.rec.xml"))

    # Map TXT files by base name (sample.rec.xml -> sample.xml.txt)
    txt_files = glob(os.path.join(txt_dir, "*.xml.txt"))
    txt_map = {}
    for f in txt_files:
        base = os.path.basename(f)
        if base.endswith(".xml.txt"):
            # sample.xml.txt → sample.rec.xml key
            key = base.replace(".xml.txt", ".rec.xml")
            txt_map[key] = f

    # Process each xml file
    for xml_file in xml_files:
        base = os.path.basename(xml_file)
        txt_file = txt_map.get(base)

        if txt_file:
            out_name = base.replace(".rec.xml", "_parsed.xml")
            out_path = os.path.join(output_dir, out_name)
            process_file(xml_file, txt_file, out_path)
        else:
            print(f"No matching TXT file for {base}")
