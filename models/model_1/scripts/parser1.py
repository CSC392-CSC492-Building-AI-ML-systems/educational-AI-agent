import sys
import os

# I run it with: python models/model_1/scripts/parser1.py data/model_0/inputs data/model_0/outputs data/model_1/parsed
if len(sys.argv) != 4:
    print("Usage: python parser1.py <xml_input_folder> <txt_input_folder> <output_folder>")
    sys.exit(1)

current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

xml_input_folder = os.path.join(current_path, sys.argv[1])
txt_input_folder = os.path.join(current_path, sys.argv[2])
output_folder = os.path.join(current_path, sys.argv[3])

os.makedirs(output_folder, exist_ok=True)


xml_files = [f for f in os.listdir(xml_input_folder) if f.endswith(".xml")]

for xml_filename in xml_files:
    xml_filepath = os.path.join(xml_input_folder, xml_filename)

    base_name = xml_filename.replace(".rec.xml", "")
    txt_filename = f"{base_name}.xml.txt"
    txt_filepath = os.path.join(txt_input_folder, txt_filename)

    with open(xml_filepath, "r") as f:
        data = f.readlines()
    if not os.path.exists(txt_filepath):
        continue
    with open(txt_filepath, "r") as f:
        counter = [int(line.strip()) for line in f]

    breaks = set(counter[i-1] for i in range(len(counter)) if counter[i] == 0)
    xml_parsed = []
    for i, line in enumerate(data):
        if i in breaks:
            xml_parsed.append("<annotation>\n</annotation>\n</event>\n<event depth=\"-2\">\n")
        elif i == 2:
            xml_parsed.append("<event depth=\"-2\">\n")
        elif i == len(data) - 1:
            xml_parsed.append("<annotation>\n</annotation>\n</event>\n")
        xml_parsed.append(line)

    parsed_filename = xml_filename.replace(".rec.xml", "_parsed.xml")
    output_filepath = os.path.join(output_folder, parsed_filename)

    with open(output_filepath, "w") as f:
        f.writelines(xml_parsed)


print("Finished!")
