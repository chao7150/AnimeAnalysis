'''
copied from https://qiita.com/gabdro/private/636c5e9e02f143b273e6 for personal study
'''

import urllib
import re
import http.client
import xml.etree.ElementTree as ET #xml
import time #sleep

from key import *

#ログイン処理
post_dict ={'show_button_facebook':'1',
    'next_url':'',
    'mail':mail,
    'password':password
}

headers = {}
headers['Referer']='https://account.nicovideo.jp/'
headers['Content-type']='application/x-www-form-urlencoded';
conn = http.client.HTTPSConnection('account.nicovideo.jp')
conn.request('POST','/api/v1/login?show_button_twitter=1&site=niconico',urllib.parse.urlencode(post_dict),headers)
rs = conn.getresponse()
mc = re.compile('(user_session=(?!deleted)[^;]*);?').search(rs.getheader('Set-Cookie'))
user_session = mc.group(1)
headers['Cookie'] = user_session
rs.read()
rs.close()
conn.close()

#動画情報の取得
videoid='sm30933340' #kemono_friends_ep1

conn = http.client.HTTPConnection('flapi.nicovideo.jp', 80)
conn.request('GET', '/api/getflv/%s' % videoid, '', headers)
rs = conn.getresponse()
body = rs.read()
rs.close()
conn.close()

qs = urllib.parse.parse_qs(body.decode('utf-8'))
thread_id = qs['thread_id'][0] #thread_id
user_id = qs['user_id'][0]
print(thread_id , user_id)
#print(body)
mc = re.compile(r'&ms=http%3A%2F%2F(.+?)\.nicovideo\.jp(%2F.+?)&').search(body.decode('utf-8'))

message_server = urllib.parse.unquote_plus(mc.group(1))
message_path = urllib.parse.unquote_plus(mc.group(2))

#公式動画以外の取得では使わない
if videoid.find("sm") == 0:
    thread_key = None
    force_184=None
    waybackkey=None
else:
    conn = http.client.HTTPConnection('flapi.nicovideo.jp', 80)
    conn.request('GET', '/api/getthreadkey?thread=%s' % videoid, '', headers)
    rs = conn.getresponse()
    body = rs.read()
    rs.close()
    conn.close()
    qs = urllib.parse.parse_qs(body.decode('utf-8'))
    thread_key = qs['threadkey'][0] #thread_id
    force_184 = qs['force_184'][0]
    print(thread_key , force_184)

    conn = http.client.HTTPConnection('flapi.nicovideo.jp', 80)
    conn.request('GET', '/api/getwaybackkey?thread=%s' % videoid, '', headers)
    rs = conn.getresponse()
    body = rs.read()
    rs.close()
    conn.close()
    qs = urllib.parse.parse_qs(body.decode('utf-8'))
    waybackkey = qs['waybackkey'][0] #thread_id
    print(waybackkey)


#動画のコメント取得
res_from=-1000 #コメントを現在から遡って何件取得してくるか
when=""
headers['Content-type'] = 'text/xml'

maxloop=2 #何回遡ってログを保存するかの回数
for loopcount in range(maxloop):
    #postXml = '<thread thread="%s" version="%s" res_from="%s" user_id="%s" threadkey="%s" force_184="%s"/>' % (thread_id,20090904,res_from,user_id,thread_key,force_184)
    postXml = '<thread thread="%s" version="%s" res_from="%s" user_id="%s" threadkey="%s" force_184="%s" when="%s" waybackkey="%s" />' % (thread_id,20090904,res_from,user_id,thread_key,force_184,when,waybackkey)

    conn = http.client.HTTPConnection('%s.nicovideo.jp' % message_server, 80)
    conn.request('POST', message_path, postXml, headers)
    rs = conn.getresponse()
    body = rs.read()
    rs.close()
    conn.close()

    #file_name = "gochiusa/tea_{}.xml".format(loopcount)
    file_name = "log/{}_{}.xml".format(videoid,loopcount)
    f = open(file_name,'w')
    f.write(body.decode('utf-8'))
    f.close()

    root = ET.fromstring(body)
    for child in root:
        if child.text !=None:
            when = child.attrib['date']
            break
    time.sleep(5)