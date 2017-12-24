import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import re

filename = 'sm13403834'
tree = ET.parse('log/' + filename + '_0.xml')
root = tree.getroot()
print(root.attrib)

coms = []
for child in root:
    t = child.text
    try:
        if re.search('[a-z]*[0-9][a-z]*', t):
            print(t)
            coms.append(int(child.attrib['vpos']))
    except:
        pass
bins = int(max(coms)/300)
print()
plt.hist(coms, bins=bins)
plt.show()
