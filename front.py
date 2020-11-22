import requests

response = requests.get('http://localhost:5000//erea/all')

print('メッセージ:{}'.format(response.text))