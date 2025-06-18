import sys
import os

# I run it with: python models/model_3/scripts/parser2.py data/model_1/outputs data/model_1/inputs data/model_3/parsed
if len(sys.argv) != 4:
    print("Usage: python your_script_name.py <plain_text_input_folder> <parsed_xml_input_folder> <output_folder>")
    sys.exit(1)

current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path)))

plain_text_input_folder = os.path.join(current_path, sys.argv[1])
parsed_xml_input_folder = os.path.join(current_path, sys.argv[2])
base_output_folder = os.path.join(current_path, sys.argv[3])

def get_file_pairs(xml_folder, txt_folder):
    if not os.path.isdir(xml_folder):
        print(f"Error: XML folder not found: {xml_folder}")
        sys.exit(1)
    if not os.path.isdir(txt_folder):
        print(f"Error: TXT folder not found: {txt_folder}")
        sys.exit(1)

    xml_files = sorted([f for f in os.listdir(xml_folder) if f.lower().endswith('.xml')])
    xml_paths = []
    txt_paths = []

    for xml_file in xml_files:
        base = os.path.splitext(xml_file)[0]
        base = base.replace('_parsed', '')
        xml_path = os.path.join(xml_folder, xml_file)
        txt_path = os.path.join(txt_folder, base + '_training.txt')

        if os.path.exists(txt_path):
            xml_paths.append(xml_path)
            txt_paths.append(txt_path)

    return xml_paths, txt_paths

parsed_xml_list, plain_text_list = get_file_pairs(parsed_xml_input_folder, plain_text_input_folder)


# Note: Each path in plain_text_list at index i corresponds to the parsed xml 
# file at index i in parsed_xml_list

def combine_xml_with_training(xml_path, training_path):
    # Read XML file
    with open(xml_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Read training data
    with open(training_path, 'r') as f:
        training_lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Track training data index
    training_idx = 0
    
    # Split XML into lines for processing
    lines = xml_content.split('\n')
    modified_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # If we find an event tag
        if '<event depth=' in line:
            if training_idx < len(training_lines):
                # Replace the depth value
                depth = training_lines[training_idx]
                modified_line = f'<event depth="{depth}">'
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
                
        # If we find an annotation tag
        elif '<annotation>' in line:
            modified_lines.append(line)  # Add the opening tag
            
            # Skip any existing content until closing tag
            while i < len(lines) and '</annotation>' not in lines[i]:
                i += 1
                
            if training_idx + 1 < len(training_lines):
                # Add the new annotation text
                modified_lines.append(training_lines[training_idx + 1])
                training_idx += 2
            else:
                training_idx += 1
                
            if i < len(lines):  # Add the closing tag
                modified_lines.append(lines[i])
        else:
            modified_lines.append(line)
        i += 1
    
    # Write output file
    xml_filename = os.path.basename(xml_path)
    output_filename = xml_filename.replace('.xml', '_combined.xml')
    output_path = os.path.join(base_output_folder, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(modified_lines))
    
    print(f"Successfully processed {xml_path}")

# Process each pair of files
for xml_path, training_path in zip(parsed_xml_list, plain_text_list):

    try:
        combine_xml_with_training(xml_path, training_path)
    except Exception as e:
        print(f"Error processing {xml_path}: {str(e)}")