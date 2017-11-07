import requests
import urllib.parse
import key

auth = {
    'mail' : key.mail,
    'password' : key.password,
    'next_url' : ''
}
headers = {
    'Referer' : 'https://account.nicovideo.jp/',
    'Content-type' : 'application/x-www-form-urlencoded'
}
s = requests.Session()
s.post('https://account.nicovideo.jp/api/v1/login', data=auth, headers=headers)

videoid = '1484126967'

r = s.get('http://flapi.nicovideo.jp/api/getflv/1484126967')
print(urllib.parse.parse_qs(r.text))
