import requests

response = requests.get('http://localhost:5000/erea/0/wakeup_people')
print('メッセージ:{}'.format(response.text))
response = requests.get('http://localhost:5000/erea/1/wakeup_people')
print('メッセージ:{}'.format(response.text))
response = requests.get('http://localhost:5000/erea/2/wakeup_people')
print('メッセージ:{}'.format(response.text))

response = requests.get('http://localhost:5000/erea/all')
print('メッセージ:{}'.format(response.text))