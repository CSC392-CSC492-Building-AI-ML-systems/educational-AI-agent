# List of paths to the model 1 output plain text files (copy relative path and paste here)
plain_text_list = ["models/Model 1/scripts/temp/1727009412_training.txt",
                   "models/Model 1/scripts/temp/1727009556_training.txt",
                   "models/Model 1/scripts/temp/1727009592_training.txt",
                   "models/Model 1/scripts/temp/first_julia_rec_training.txt",
                   "models/Model 1/scripts/temp/rene.annotated1_training.txt",
                   "models/Model 1/scripts/temp/renee_rec2_training.txt"]

# List of paths to the model 1 input parsed xml files (copy relative path and paste here)
parsed_xml_list = ["models/Model 1/scripts/temp/1727009412_parsed.xml",
                   "models/Model 1/scripts/temp/1727009556_parsed.xml",
                   "models/Model 1/scripts/temp/1727009592_parsed.xml",
                   "models/Model 1/scripts/temp/first_julia_rec_parsed.xml",
                   "models/Model 1/scripts/temp/rene.annotated1_parsed.xml",
                   "models/Model 1/scripts/temp/renee_rec2_parsed.xml"]

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
    output_path = xml_path.replace('.xml', '_combined.xml')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(modified_lines))
    
    print(f"Successfully processed {xml_path}")

# Process each pair of files
for xml_path, training_path in zip(parsed_xml_list, plain_text_list):
    try:
        combine_xml_with_training(xml_path, training_path)
    except Exception as e:
        print(f"Error processing {xml_path}: {str(e)}")