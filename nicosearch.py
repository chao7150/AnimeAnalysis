import requests

url = 'http://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'
headers = {
    'User-Agent' : 'chao'
}
params = {
    'q' : '少女終末旅行',
    'targets' : 'title',
    'fields' : 'contentId,title',
    '_sort' : '-viewCounter',
    '_context' : ''
}

res = requests.get(url, params=params, headers=headers)
print(res.json())