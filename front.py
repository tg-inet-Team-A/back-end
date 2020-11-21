import requests

response = requests.get('http://localhost:5000/hello')

print('httpステータス:{}, メッセージ:{}'.format(response.status_code, response.text))