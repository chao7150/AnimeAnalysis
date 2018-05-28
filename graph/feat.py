import csv
import time
import mediawiki

directors = []
with open("directors.csv", "r")as f:
    reader = csv.reader(f, dialect="excel")
    for row in reader:
        directors.append(row)

ans = []
for i, x in enumerate(directors[4:]):
    x = x[0]
    for y in directors[i+5:]:
        y = y[0]
        time.sleep(3)
        hits = mediawiki.hitNum("{0} {1} -日本のアニメ映画作品一覧 -アニメの賞 -日本のアニメスタジオ -日本のアニメーション監督 -アニメ関連の一覧 -作品の一覧".format(x, y))
        print(x, y, hits)
        ans.append([x, y, hits])

with open("combinations.csv", "w")as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerows(ans)