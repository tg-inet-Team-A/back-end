import requests

response = requests.get('http://localhost:5000/erea/0000/wakeup_people')

print('メッセージ:{}'.format(response.text))