import xml.etree.ElementTree as ET

filename = input('movie id: ')
tree = ET.parse('log/' + filename + '_0.xml')
root = tree.getroot()

for child in root:
    print(child.text)