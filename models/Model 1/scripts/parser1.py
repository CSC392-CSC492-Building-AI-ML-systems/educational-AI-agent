import sys

if len(sys.argv) != 3:
    print("Usage: python parser1.py <xml> <txt>")
    sys.exit(1)

xml = sys.argv[1]
txt = sys.argv[2]

with open(xml, "r") as f:
    xml_data = f.readlines()

with open(txt, "r") as f:
    counter = [int(line.strip()) for line in f]

breaks = set(counter[i-1] for i in range(len(counter)) if counter[i] == 0)

xml_parsed = []
for i, line in enumerate(xml_data):
    if i in breaks:
        xml_parsed.append("<annotation>\n</annotation>\n</event>\n<event depth=\"-1\">\n")
    elif i == 2:
        xml_parsed.append("<event depth=\"-1\">\n")
    elif i == len(xml_data) - 1:
        xml_parsed.append("<annotation>\n</annotation>\n</event>\n")
    xml_parsed.append(line)

with open(f"output/{xml[:-4]}_parsed.xml", "w") as f:
    f.writelines(xml_parsed)

print(f"Parsed XML saved as {xml[:-4]}_parsed.xml")
