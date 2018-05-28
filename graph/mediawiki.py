import requests
from html.parser import HTMLParser

def hitNum(query):
    URL = "http://ja.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query.encode("UTF-8"),
        "format": "xml"
    }

    response = requests.get(URL, params)
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "searchinfo":
                self.hits = attrs[0][1]
    parser = MyHTMLParser()
    parser.feed(response.text)
    return parser.hits

if __name__ == "__main__":
    print(hitNum("ちゃお"))