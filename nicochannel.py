import requests
from html.parser import HTMLParser
import os

class nicoHtmlParser(HTMLParser):
    def __init__(self):
        super(nicoHtmlParser, self).__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if 'class' in attrs_dict and attrs_dict['class'] == 'g-video-link':
            if not 'PV' in attrs_dict['title']:
                self.urls.append((attrs_dict['title'], attrs_dict['href']))

def getList(url):
    r = requests.get(url)
    parser = nicoHtmlParser()
    parser.feed((r.text))
    urls_uniq = []
    for u in parser.urls:
        if u not in urls_uniq:
            urls_uniq.append(u)
    return urls_uniq

if __name__ == '__main__':
    print(getList('http://ch.nicovideo.jp/darli-fra'))

 