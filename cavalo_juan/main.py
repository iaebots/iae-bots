import requests
import os
import requests
import random

API_KEY = str(os.environ.get('IAE_CAVALOJUAN_APIKEY'))
API_SECRET = str(os.environ.get('IAE_CAVALOJUAN_APISECRET'))

url = 'https://api.iaebots.com/api/v1/posts'

cavalo = ['C','A','V','A','L','O']
juan = ['J','U','A','N']

random.shuffle(cavalo)
random.shuffle(juan)
quote = ''.join(cavalo) + " " +''.join(juan)

data = {'body': quote}
print(quote)
if quote == 'CAVALO JUAN':
  juan = open('juan.jpg', 'rb')
  file = {'media': juan}
  response = requests.post(url, data=data, files=file,  headers={
                'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})
  juan.close()
  os.remove('main.py')
else:
  response = requests.post(url, data=data,  headers={
                'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})

print(response)