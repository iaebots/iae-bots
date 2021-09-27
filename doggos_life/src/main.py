import random
import os
import datetime
import requests

# key pair for API authentication
API_KEY = os.environ['DOGGOS_API_KEY']
API_SECRET = os.environ['DOGGOS_API_SECRET']

def create_post(data=None, file=None):
  url = 'https://api.iaebots.com/api/v1/posts'

  requests.post(url, headers={'Authorization': 'Token api_key=' +
                                API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)

hour = datetime.datetime.now().hour

# odd hour, get random dog content from random.dog
if hour % 2 != 0:
  doggos_list = []

  with open('../res/doggos.txt', 'r') as f:
    doggos_list = f.readlines()
    f.close()

  i = random.randrange(0, len(doggos_list) - 1)
  
  try:
    response = requests.get('https://random.dog/' + doggos_list[i].replace('\n', ''))
    
    if response.status_code == 200:
        file = { 'media': response.content }
        create_post(file=file)
  except Exception as e:
      print(e)
      exit(1)
else:
  facts = []

  with open('../res/dog_facts.txt', 'r') as f:
    facts = f.readlines()
    f.close()

  i = random.randrange(0, len(facts) - 1)

  try:
    response = requests.get('https://dog.ceo/api/breeds/image/random')

    if response.status_code == 200:
      data = response.json()
      r_2 = requests.get(data['message'])
      data = { 'body': facts[i].replace('\n', '') }
      file = { 'media': r_2.content }
      create_post(data=data, file=file)
  except Exception as e:
    print(e)
    exit(1)
