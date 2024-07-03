import xml.etree.ElementTree as ET
import xmltodict
import json

tree = ET.parse('service_statistics.xml')
root = tree.getroot()

print(root)

for child in root:
    print(child.tag, child.attrib)



with open('service_statistics.xml') as f:
    xml_str=f.read()

print(xml_str)
xml_dict = xmltodict.parse(xml_str)
print(xml_dict)

json_str = json.dumps(xml_dict, indent=4)
print(json_str)


with open('node_statistics.xml') as f:
    xml_str = f.read()

print(xml_str)
xml_dict = xmltodict.parse(xml_str)
print(xml_dict)

json_str = json.dumps(xml_dict, indent=4)
print(json_str)
