xml = "1727009412.xml"
txt = "1727009412.xml.txt"

with open(xml, "r") as f:
    xml_data = f.readlines()

with open(txt, "r") as f:
    counter = [int(line.strip()) for line in f]

breaks = set(counter[i-1] for i in range(len(counter)) if counter[i] == 0)

xml_parsed = []
for i, line in enumerate(xml_data):
    if i in breaks:
        xml_parsed.append("<annotation>\n")
        xml_parsed.append("</annotation>\n")
        xml_parsed.append("</event>\n")
        xml_parsed.append("<event>\n")
    elif i == 2:
        xml_parsed.append("<event>\n")
    elif i == len(xml_data) - 1:
        xml_parsed.append("</event>\n")
    xml_parsed.append(line)

with open("parsed.xml", "w") as f:
    f.writelines(xml_parsed)

