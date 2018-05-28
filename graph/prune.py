import csv
import sys
import requests
import urllib.parse
import re
import time

directors = []
directors_pruned = []
with open("directors.csv", "r")as f:
    reader = csv.reader(f, dialect="excel")
    for row in reader:
        directors.append(row)
        
URL = "http://seesaawiki.jp/w/radioi_34/search"
for x in directors:
    time.sleep(3)
    params = {
        "keywords": x[0].encode("euc-jp"),
        "search_target": "all"
    }
    response = requests.get(URL, params)
    if response.text.find("見つかりませんでした") != -1:
        print("not found")
    else:
        directors_pruned.append(x)
        print(re.findall(r"全文検索\S*。", response.text)[0])
print(directors_pruned)
