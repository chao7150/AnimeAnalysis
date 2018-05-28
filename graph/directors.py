import requests
import re
import csv

r = requests.get("https://www.animatetimes.com/tag/details.php?id=6631")
d = re.findall(r"\n監督\S*[<BR>, <br>]", r.text)
d = [x.replace("\n", "").replace("<BR>", "").replace("<br>", "") for x in d]
d = [x[x.find("：")+1:] for x in d]
d = [x for x in d if " " not in x]
d = [[x] for x in d if "、" not in x]
print(d)

with open("directors.csv", "w")as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(d)