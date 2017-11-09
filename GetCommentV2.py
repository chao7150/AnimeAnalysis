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
lin = s.post('https://account.nicovideo.jp/api/v1/login', data=auth, headers=headers)
videoid = '1484126967'

r = s.get('http://flapi.nicovideo.jp/api/getflv/1484126967')
p = urllib.parse.parse_qs(r.text)
thread_id = p['thread_id'][0]
user_id = p['user_id'][0]
message_server = p['ms'][0]
res_from = -1000
print(message_server, thread_id, user_id)
headers['Content-type'] = 'text/xml'
postXml = '<thread thread="%s" version="%s" res_from="%s" user_id="%s" threadkey="%s" force_184="%s" when="%s" waybackkey="%s" />' % (thread_id,20090904,res_from,user_id, '', '', '', '')
com = s.post(message_server, data=postXml, headers=headers)
print(com.text)